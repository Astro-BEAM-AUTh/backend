"""Supabase JWT verification and authenticated user helpers."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from typing import TYPE_CHECKING, Any

import jwt
from fastapi import Header, HTTPException, status
from jwt import PyJWKClient
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from backend.configs.config import settings
from backend.models import User, UserCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("astro_backend")


@dataclass(slots=True)
class AuthPrincipal:
    """Verified Supabase authentication payload."""

    subject: str
    email: str
    username: str
    provider: str = "supabase"
    claims: dict[str, Any] | None = None


def _normalize_username(source: str) -> str:
    """
    Normalize an email local part into a safe username format.
    This is a simple heuristic that lowercases the input and replaces non-alphanumeric characters with underscores.
    If the resulting string is empty, it defaults to 'astro_user'.
    """
    normalized = "".join(ch if ch.isalnum() else "_" for ch in source.lower()).strip("_")
    return normalized or "astro_user"


def _derive_username(email: str, subject: str) -> str:
    """
    Derive a stable username from the email local part and a hash of the subject claim.
    This approach ensures that the same user gets the same username across sessions, while avoiding collisions by incorporating a hash of the subject claim.

    Args:
        email: The user's email address from the JWT claims
        subject: The 'sub' claim from the JWT, which is a unique identifier for the user in Supabase

    Returns:
        A normalized username string derived from the email and subject claim
    """
    local_part = email.split("@", 1)[0] if email else "astro_user"
    digest = sha256(subject.encode("utf-8")).hexdigest()[:8]
    return f"{_normalize_username(local_part)}_{digest}"


@lru_cache(maxsize=1)
def _jwks_client() -> PyJWKClient:
    """
    Get a cached PyJWKClient instance for fetching JWKS keys.

    Raises:
        RuntimeError: If the Supabase JWKS URL is not configured

    Returns:
        PyJWKClient: A cached PyJWKClient instance
    """
    jwks_url = settings.supabase_jwks_endpoint
    if not jwks_url:
        msg = "Supabase JWKS URL is not configured"
        raise RuntimeError(msg)

    return PyJWKClient(jwks_url)


def _decode_supabase_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a Supabase JWT, returning the claims if valid.

    Args:
        token (str): The JWT token to decode and verify

    Raises:
        RuntimeError: If the Supabase issuer URL is not configured
        ValueError: If the JWT header is missing the algorithm

    Returns:
        dict[str, Any]: The decoded JWT claims
    """
    issuer = settings.supabase_issuer_url
    if not issuer:
        msg = "Supabase issuer URL is not configured"
        raise RuntimeError(msg)

    # Get the algorithm from the JWT header
    header = jwt.get_unverified_header(token)
    algorithm = header.get("alg")
    if not algorithm:
        msg = "JWT header missing algorithm"
        raise ValueError(msg)

    signing_key: jwt.PyJWK = _jwks_client().get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=[signing_key.algorithm_name],
        audience=settings.supabase_audience,
        issuer=issuer,
        options={"require": ["exp", "iat", "sub"]},
    )


async def get_optional_principal(authorization: str | None = Header(default=None)) -> AuthPrincipal | None:
    """
    Return a verified Supabase principal if the request carries a bearer token.

    Args:
        authorization (str | None): The authorization header from the request

    Returns:
        AuthPrincipal | None: The verified principal or None if no valid token is provided
    """
    if not authorization:
        return None

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        logger.warning("Invalid authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    try:
        claims = _decode_supabase_token(token.strip())
    except Exception as exc:
        logger.warning("Failed to decode Supabase token: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        ) from exc

    subject = str(claims.get("sub", "")).strip()
    email = str(claims.get("email", "")).strip()
    if not subject or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing required claims",
        )

    return AuthPrincipal(subject=subject, email=email, username=_derive_username(email, subject), claims=claims)


def build_guest_user(requestor: UserCreate) -> UserCreate:
    """Normalize a guest requestor payload for persistence."""
    return UserCreate(
        user_id=requestor.user_id,
        username=requestor.username,
        email=requestor.email,
        auth_provider="guest",
    )


def build_user_from_principal(principal: AuthPrincipal) -> UserCreate:
    """Map a verified principal to the local user payload shape."""
    return UserCreate(
        user_id=principal.subject,
        username=principal.username,
        email=principal.email,
        auth_provider=principal.provider,
    )


async def get_local_user_by_user_id(db: AsyncSession, user_id: str) -> User | None:
    """
    Return a local user by stable external user id.

    Args:
        db: Database session dependency
        user_id: The external user ID to look up (e.g. Supabase 'sub' claim)

    Returns:
        User | None: The local user if found, otherwise None
    """
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_local_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Return a local user by email address.

    Args:
        db: Database session dependency
        email: The email address to look up

    Returns:
        User | None: The local user if found, otherwise None
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_local_user(db: AsyncSession, requestor: UserCreate) -> User:
    """
    Create a local user row.

    Args:
        db: Database session dependency
        requestor: The user creation payload

    Returns:
        User: The created local user
    """
    user = User(**requestor.model_dump())
    db.add(user)
    await db.flush()
    return user


async def get_or_create_local_user_from_principal(db: AsyncSession, principal: AuthPrincipal) -> User:
    """
    Get or create local user for a verified principal.

    Args:
        db: Database session dependency
        principal: The verified Supabase principal

    Returns:
        User: The local user
    """
    existing_user = await get_local_user_by_user_id(db, principal.subject)
    if existing_user is not None:
        return existing_user

    try:
        return await create_local_user(db, build_user_from_principal(principal))
    except IntegrityError as exc:
        logger.warning("User creation failed due to integrity error: %s", exc)
        logger.info("Attempting to update existing user with matching email")
        await db.rollback()
        existing_user = await get_local_user_by_email(db, principal.email)
        if existing_user is not None:
            existing_user.user_id = principal.subject
            existing_user.username = principal.username
            existing_user.auth_provider = principal.provider
            db.add(existing_user)
            await db.flush()
            return existing_user


async def get_or_create_guest_user(db: AsyncSession, requestor: UserCreate) -> User:
    """
    Get or create local user for a guest submission.

    Args:
        db: Database session dependency
        requestor: The guest user creation payload

    Returns:
        User: The local user
    """
    guest_user = build_guest_user(requestor)
    existing_user = await get_local_user_by_user_id(db, guest_user.user_id)
    if existing_user is not None:
        return existing_user

    try:
        return await create_local_user(db, guest_user)
    except IntegrityError as exc:
        logger.warning("User creation failed due to integrity error: %s", exc)
        await db.rollback()
        existing_user = await get_local_user_by_email(db, requestor.email)
        if existing_user is not None:
            return existing_user
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from exc
