"""Type definitions for SchedulifyX SDK v3.0 — Three-Tier Architecture"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==================== COMMON ====================

@dataclass
class PaginatedResponse:
    """A paginated API response"""
    data: List[Any] = field(default_factory=list)
    pagination: Optional[dict] = field(default_factory=lambda: {"total": 0, "limit": 20, "offset": 0})


# ==================== TIER 1: TENANTS ====================

@dataclass
class Tenant:
    """A tenant represents a user in your application"""
    id: str
    external_id: str
    created_at: str
    is_active: bool = True
    email: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    updated_at: Optional[str] = None
    connected_accounts: Optional[int] = None
    total_posts: Optional[int] = None


@dataclass
class TenantAccount:
    """A social account connected by a tenant"""
    id: str
    platform: str
    account_name: str
    account_username: str
    is_active: bool
    followers_count: int
    created_at: str
    avatar_url: Optional[str] = None
    following_count: Optional[int] = None
    media_count: Optional[int] = None


@dataclass
class ClientToken:
    """A short-lived token for embedding UI components"""
    token: str
    expires_at: str
    expires_in: int
    components: List[str] = field(default_factory=list)
    origins: List[str] = field(default_factory=list)
    usage: Optional[Dict[str, str]] = None


# ==================== TIER 1: WEBHOOKS ====================

@dataclass
class Webhook:
    """A webhook configuration"""
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
    stats: Optional[Dict[str, int]] = None


@dataclass
class WebhookEvent:
    """A webhook delivery event"""
    id: str
    webhook_id: str
    event_type: str
    status: str  # 'pending' | 'delivered' | 'failed'
    attempts: int
    created_at: str
    response_status: Optional[int] = None
    response_time_ms: Optional[int] = None
    error_message: Optional[str] = None
    delivered_at: Optional[str] = None


@dataclass
class WebhookEventType:
    """An available webhook event type"""
    event: str
    category: str
    action: str
    description: str


# ==================== TIER 1: USAGE ====================

@dataclass
class Usage:
    """API usage statistics"""
    requests_today: int
    rate_limit_per_min: int
    monthly_requests: int
    monthly_limit: int
    monthly_remaining: int
    social_sets: Dict[str, Any] = field(default_factory=dict)
    last_used_at: Optional[str] = None
    resets_at: Optional[str] = None


# ==================== TIER 2: POSTS ====================

@dataclass
class PostPlatform:
    """Platform-specific post data"""
    platform: str
    account_id: Optional[str] = None
    status: Optional[str] = None
    platform_post_id: Optional[str] = None
    platform_post_url: Optional[str] = None
    error: Optional[str] = None
    platform_settings: Optional[Dict[str, Any]] = None


@dataclass
class Post:
    """A social media post"""
    id: str
    content: str
    status: str  # 'draft' | 'scheduled' | 'publishing' | 'published' | 'failed'
    created_at: str
    scheduled_for: Optional[str] = None
    published_at: Optional[str] = None
    source: Optional[str] = None
    post_type: str = 'post'
    is_draft: bool = False
    is_thread: bool = False
    tenant_user_id: Optional[str] = None
    updated_at: Optional[str] = None
    platforms: List[PostPlatform] = field(default_factory=list)


# ==================== TIER 2: ACCOUNTS ====================

@dataclass
class Account:
    """A connected social account"""
    id: str
    platform: str
    account_name: str
    account_username: str
    is_active: bool
    followers_count: int
    created_at: str
    avatar_url: str = ''
    tenant_user_id: Optional[str] = None


@dataclass
class AccountDetail(Account):
    """Detailed social account information"""
    platform_account_id: str = ''
    following_count: int = 0
    media_count: int = 0
    bio: Optional[str] = None
    website: Optional[str] = None
    is_verified: bool = False
    profile_url: Optional[str] = None


# ==================== TIER 2: ANALYTICS ====================

@dataclass
class AnalyticsOverview:
    """High-level analytics overview"""
    total_posts: int = 0
    published_posts: int = 0
    scheduled_posts: int = 0
    connected_accounts: int = 0
    total_followers: Optional[int] = None
    accounts: Optional[List[Dict[str, Any]]] = None


@dataclass
class AccountAnalyticsEntry:
    """A single analytics data point for an account"""
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    total_views: int = 0
    engagement_rate: float = 0.0
    recorded_at: str = ''


@dataclass
class DetailedAnalytics:
    """Detailed analytics with post/account/engagement breakdowns"""
    posts: Optional[Dict[str, int]] = None
    accounts: Optional[List[Dict[str, Any]]] = None
    engagement: Optional[Dict[str, Any]] = None


# ==================== TIER 2: MEDIA ====================

@dataclass
class MediaItem:
    """A media library item"""
    id: str
    file_name: str
    file_type: str  # 'image' | 'video' | 'audio'
    mime_type: str
    created_at: str
    updated_at: str
    file_size: Optional[int] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None
    folder: str = '/'
    alt_text: Optional[str] = None


# ==================== TIER 2: QUEUE ====================

@dataclass
class QueueSlot:
    """A single queue time slot"""
    day_of_week: int
    time: str


@dataclass
class QueueSchedule:
    """A queue schedule for a social account"""
    id: str
    account_id: str
    timezone: str
    is_active: bool
    created_at: str
    updated_at: str
    slots: List[QueueSlot] = field(default_factory=list)
    account: Optional[Dict[str, str]] = None


# ==================== TIER 2: PROFILES ====================

@dataclass
class Profile:
    """A posting profile/category"""
    id: str
    name: str
    created_at: str
    description: Optional[str] = None
    color: str = '#6366f1'
    is_default: bool = False
    updated_at: Optional[str] = None


# ==================== TIER 2: X/TWITTER ====================

@dataclass
class XConfig:
    """X/Twitter configuration"""
    has_byok_credentials: bool = False
    accounts: List[Dict[str, Any]] = field(default_factory=list)
    info: Optional[Dict[str, Any]] = None


# ==================== TIER 3: COMMENTS ====================

@dataclass
class Comment:
    """A social media comment"""
    id: str
    platform_comment_id: str
    platform: str
    created_at: str
    message: Optional[str] = None
    author_name: Optional[str] = None
    author_username: Optional[str] = None
    author_profile_picture: str = ''
    like_count: int = 0
    reply_count: int = 0
    sentiment: Optional[str] = None  # 'positive' | 'negative' | 'neutral'
    moderation_status: str = 'pending'
    is_hidden: bool = False
    post_id: Optional[str] = None
    parent_comment_id: Optional[str] = None
    platform_created_at: str = ''


@dataclass
class CommentReply:
    """A reply sent to a comment"""
    id: str
    comment_id: str
    message: str
    status: str
    created_at: str


@dataclass
class CommentStats:
    """Comment statistics"""
    total: int = 0
    by_sentiment: Optional[Dict[str, int]] = None
    hidden: int = 0
    replied: int = 0


# ==================== TIER 3: INBOX ====================

@dataclass
class Conversation:
    """A DM conversation"""
    id: str
    platform: str
    status: str
    unread_count: int
    created_at: str
    social_account_id: Optional[str] = None
    participant_name: Optional[str] = None
    participant_username: Optional[str] = None
    participant_profile_picture: Optional[str] = None
    last_message_at: Optional[str] = None


@dataclass
class Message:
    """A direct message"""
    id: str
    direction: str  # 'inbound' | 'outbound'
    message: str
    sender_name: str
    sender_username: str
    platform_message_id: str
    platform_created_at: str
    created_at: str


@dataclass
class InboxStats:
    """Inbox statistics"""
    conversations: Optional[Dict[str, int]] = None
    messages: Optional[Dict[str, Any]] = None


# ==================== TIER 3: MENTIONS ====================

@dataclass
class Mention:
    """A social media mention"""
    id: str
    platform: str
    mention_type: str
    author_username: str
    author_name: str
    content: str
    permalink: str
    created_at: str
    author_profile_picture: str = ''
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    like_count: int = 0
    comment_count: int = 0
    status: str = 'unread'
    is_ugc_saved: bool = False


@dataclass
class MentionStats:
    """Mention statistics"""
    total: int = 0
    unread: int = 0
    responded: int = 0
    ugc_saved: int = 0

