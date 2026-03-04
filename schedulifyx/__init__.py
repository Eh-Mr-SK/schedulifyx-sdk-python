"""
SchedulifyX SDK v3.0 - Official Python SDK for SchedulifyX API
Three-tier architecture: Embed, Publishing, and Full Engagement.
https://app.schedulifyx.com/docs/
"""

from .client import SchedulifyX, SchedulifyXError
from .types import (
    # Common
    PaginatedResponse,
    # Tier 1
    Tenant,
    TenantAccount,
    ClientToken,
    Webhook,
    WebhookEvent,
    WebhookEventType,
    Usage,
    # Tier 2
    Post,
    PostPlatform,
    Account,
    AccountDetail,
    AnalyticsOverview,
    AccountAnalyticsEntry,
    DetailedAnalytics,
    MediaItem,
    QueueSlot,
    QueueSchedule,
    Profile,
    XConfig,
    # Tier 3
    Comment,
    CommentReply,
    CommentStats,
    Conversation,
    Message,
    InboxStats,
    Mention,
    MentionStats,
)

__version__ = "3.0.0"
__all__ = [
    "SchedulifyX",
    "SchedulifyXError",
    "PaginatedResponse",
    # Tier 1
    "Tenant",
    "TenantAccount",
    "ClientToken",
    "Webhook",
    "WebhookEvent",
    "WebhookEventType",
    "Usage",
    # Tier 2
    "Post",
    "PostPlatform",
    "Account",
    "AccountDetail",
    "AnalyticsOverview",
    "AccountAnalyticsEntry",
    "DetailedAnalytics",
    "MediaItem",
    "QueueSlot",
    "QueueSchedule",
    "Profile",
    "XConfig",
    # Tier 3
    "Comment",
    "CommentReply",
    "CommentStats",
    "Conversation",
    "Message",
    "InboxStats",
    "Mention",
    "MentionStats",
]
