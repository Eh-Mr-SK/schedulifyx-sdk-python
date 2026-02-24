"""Type definitions for SchedulifyX SDK"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class Post:
    id: str
    content: str
    status: str  # 'draft' | 'scheduled' | 'publishing' | 'published' | 'failed'
    account_ids: List[str]
    created_at: str
    updated_at: str
    media_urls: Optional[List[str]] = None
    publish_at: Optional[str] = None
    platform_overrides: Optional[Dict[str, Dict[str, str]]] = None


@dataclass
class Account:
    id: str
    platform: str
    platform_account_id: str
    name: str
    is_active: bool
    created_at: str
    username: Optional[str] = None
    profile_picture: Optional[str] = None


@dataclass
class Analytics:
    account_id: str
    followers: int
    following: int
    posts: int
    engagement: float
    updated_at: str


@dataclass
class AnalyticsOverview:
    total_posts: int
    scheduled_posts: int
    published_posts: int
    failed_posts: int
    total_accounts: int
    active_accounts: int


@dataclass
class Usage:
    requests_today: int
    daily_limit: int
    remaining_today: int
    monthly_requests: int
    last_used_at: Optional[str]


@dataclass
class Tenant:
    id: str
    external_id: str
    created_at: str
    email: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Profile:
    id: str
    name: str
    created_at: str
    description: Optional[str] = None
    color: Optional[str] = None
    is_default: bool = False
    subscription_plan: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class QueueSlot:
    day_of_week: int  # 0-6, Sunday = 0
    time: str  # HH:MM format


@dataclass
class QueueSchedule:
    id: str
    profile_id: str
    timezone: str
    slots: List[QueueSlot]
    active: bool


@dataclass
class PaginatedResponse:
    data: List[Any]
    total: int
    limit: int
    offset: int
    has_more: bool


@dataclass
class Comment:
    id: str
    platform_comment_id: str
    platform: str
    message: str
    author_name: str
    like_count: int
    reply_count: int
    is_hidden: bool
    created_at: str
    author_username: Optional[str] = None
    author_profile_picture: Optional[str] = None
    sentiment: Optional[str] = None
    moderation_status: Optional[str] = None
    post_id: Optional[str] = None
    parent_comment_id: Optional[str] = None
    platform_created_at: Optional[str] = None


@dataclass
class CommentReply:
    id: str
    comment_id: str
    message: str
    status: str
    created_at: str


@dataclass
class CommentStats:
    total: int
    by_sentiment: Dict[str, int]
    hidden: int
    replied: int


@dataclass
class Conversation:
    id: str
    platform: str
    participant_name: str
    social_account_id: str
    status: str
    unread_count: int
    created_at: str
    participant_username: Optional[str] = None
    participant_avatar: Optional[str] = None
    last_message_at: Optional[str] = None


@dataclass
class InboxMessage:
    id: str
    direction: str
    message: str
    created_at: str
    sender_name: Optional[str] = None
    sender_username: Optional[str] = None
    platform_message_id: Optional[str] = None
    platform_created_at: Optional[str] = None


@dataclass
class InboxStats:
    conversations: Dict[str, int]
    messages: Dict[str, Any]


@dataclass
class Mention:
    id: str
    platform: str
    mention_type: str
    author_username: str
    status: str
    is_ugc_saved: bool
    created_at: str
    like_count: int = 0
    comment_count: int = 0
    author_name: Optional[str] = None
    author_profile_url: Optional[str] = None
    content: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    permalink: Optional[str] = None


@dataclass
class MentionStats:
    total: int
    unread: int
    responded: int
    ugc_saved: int


@dataclass
class Webhook:
    id: str
    name: str
    url: str
    events: List[str]
    is_active: bool
    retry_count: int
    timeout_seconds: int
    created_at: str
    updated_at: str
    secret: Optional[str] = None
    last_triggered_at: Optional[str] = None
    last_success_at: Optional[str] = None
    last_failure_at: Optional[str] = None
