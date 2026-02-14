"""
SchedulifyX SDK - Official Python SDK for SchedulifyX API
https://app.schedulifyx.com/docs/
"""

from .client import SchedulifyX, SchedulifyXError
from .types import (
    Post,
    Account,
    Analytics,
    AnalyticsOverview,
    Usage,
    Tenant,
    QueueSlot,
    QueueSchedule,
    MediaUploadResponse,
    PaginatedResponse,
    Comment,
    CommentReply,
    CommentStats,
    Conversation,
    InboxMessage,
    InboxStats,
    HashtagSetItem,
    HashtagSet,
    GeneratedHashtag,
    Template,
    Webhook,
)

__version__ = "1.1.0"
__all__ = [
    "SchedulifyX",
    "SchedulifyXError",
    "Post",
    "Account",
    "Analytics",
    "AnalyticsOverview",
    "Usage",
    "Tenant",
    "QueueSlot",
    "QueueSchedule",
    "MediaUploadResponse",
    "PaginatedResponse",
    "Comment",
    "CommentReply",
    "CommentStats",
    "Conversation",
    "InboxMessage",
    "InboxStats",
    "HashtagSetItem",
    "HashtagSet",
    "GeneratedHashtag",
    "Template",
    "Webhook",
]
