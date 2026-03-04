"""
SchedulifyX API Client v3.0

Three-Tier Architecture:
- Tier 1 (Embed): Tenants, webhooks, usage, client tokens
- Tier 2 (Publishing): Posts, accounts, analytics, media, queue, profiles, X/Twitter
- Tier 3 (Full Engagement): Comments, inbox, mentions

Available API Scopes:
  T1: tenants:read, tenants:write, webhooks:read, webhooks:write
  T2: posts:read, posts:write, posts:publish, accounts:read, analytics:read,
      media:read, media:write, queue:read, queue:write, profiles:read, profiles:write
  T3: comments:read, comments:write, inbox:read, inbox:write, mentions:read
"""

import requests
from typing import Any, Dict, List, Optional, TypeVar, Type

from .types import (
    Tenant,
    TenantAccount,
    ClientToken,
    Webhook,
    WebhookEvent,
    WebhookEventType,
    Usage,
    PaginatedResponse,
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
    Comment,
    CommentReply,
    CommentStats,
    Conversation,
    Message,
    InboxStats,
    Mention,
    MentionStats,
)


class SchedulifyXError(Exception):
    """Exception raised for SchedulifyX API errors"""
    
    def __init__(self, message: str, code: str, status: int, details: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.details = details or {}
    
    def __str__(self):
        return f"SchedulifyXError({self.code}): {self.message}"


# =============================================
# Response parsing helpers
# =============================================

T = TypeVar('T')


def _snake_case(name: str) -> str:
    """Convert camelCase to snake_case."""
    import re
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()


def _to_snake_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively convert camelCase dict keys to snake_case."""
    result: Dict[str, Any] = {}
    for key, value in d.items():
        snake_key = _snake_case(key)
        if isinstance(value, dict):
            result[snake_key] = _to_snake_dict(value)
        elif isinstance(value, list):
            result[snake_key] = [_to_snake_dict(v) if isinstance(v, dict) else v for v in value]
        else:
            result[snake_key] = value
    return result


def _parse(cls: Type[T], data: Dict[str, Any]) -> T:
    """Parse a dict into a dataclass, ignoring unknown fields and converting camelCase keys."""
    import dataclasses
    snake_data = _to_snake_dict(data)
    field_names = {f.name for f in dataclasses.fields(cls)}
    filtered = {k: v for k, v in snake_data.items() if k in field_names}
    try:
        return cls(**filtered)
    except TypeError as e:
        raise SchedulifyXError(
            message=f"Failed to parse {cls.__name__}: {e}",
            code='parse_error',
            status=0,
        )


def _parse_list(cls: Type[T], items: List[Dict[str, Any]]) -> List[T]:
    """Parse a list of dicts into a list of dataclass instances."""
    return [_parse(cls, item) for item in items]


class TenantsAPI:
    """
    Tenants API — Manage users (tenants) in your multi-tenant integration.
    
    Each tenant maps to a user in your application and can connect social accounts
    and use embedded UI components.
    """
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None
    ) -> PaginatedResponse:
        """List all tenants. Returns PaginatedResponse with data as list of Tenant."""
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if search:
            params['search'] = search
        raw = self._client._request('GET', '/tenants', params=params)
        items = _parse_list(Tenant, raw.get('data', []))
        pagination = raw.get('pagination')
        return PaginatedResponse(data=items, pagination=pagination)
    
    def get(self, tenant_id: str) -> Tenant:
        """Get a single tenant"""
        raw = self._client._request('GET', f'/tenants/{tenant_id}')
        return _parse(Tenant, raw.get('data', raw))
    
    def create(
        self,
        external_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tenant:
        """Create a new tenant (maps to a user in your app)"""
        data: Dict[str, Any] = {'externalId': external_id}
        if email:
            data['email'] = email
        if name:
            data['name'] = name
        if metadata:
            data['metadata'] = metadata
        raw = self._client._request('POST', '/tenants', json=data)
        return _parse(Tenant, raw.get('data', raw))
    
    def update(
        self,
        tenant_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None
    ) -> Tenant:
        """Update a tenant"""
        data: Dict[str, Any] = {}
        if email is not None:
            data['email'] = email
        if name is not None:
            data['name'] = name
        if metadata is not None:
            data['metadata'] = metadata
        if is_active is not None:
            data['isActive'] = is_active
        raw = self._client._request('PATCH', f'/tenants/{tenant_id}', json=data)
        return _parse(Tenant, raw.get('data', raw))
    
    def delete(self, tenant_id: str) -> Dict[str, Any]:
        """Delete a tenant and all their data"""
        return self._client._request('DELETE', f'/tenants/{tenant_id}')
    
    def get_connect_url(
        self,
        tenant_id: str,
        platform: str,
        redirect_uri: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get OAuth URL for tenant to connect a social platform.
        Redirect tenant's browser to this URL to start the OAuth flow.
        Account connection is permanent — survives client token expiry.
        """
        params: Dict[str, Any] = {}
        if redirect_uri:
            params['redirectUri'] = redirect_uri
        return self._client._request(
            'GET', f'/tenants/{tenant_id}/connect/{platform}',
            params=params if params else None
        )
    
    def list_accounts(self, tenant_id: str) -> List[TenantAccount]:
        """List tenant's connected social accounts"""
        raw = self._client._request('GET', f'/tenants/{tenant_id}/accounts')
        return _parse_list(TenantAccount, raw.get('data', []))
    
    def disconnect_account(self, tenant_id: str, account_id: str) -> Dict[str, Any]:
        """Disconnect a tenant's social account"""
        return self._client._request('DELETE', f'/tenants/{tenant_id}/accounts/{account_id}')
    
    def connect_bluesky(
        self,
        tenant_id: str,
        identifier: str,
        app_password: str
    ) -> TenantAccount:
        """Connect Bluesky account for tenant (no OAuth — uses app password)"""
        raw = self._client._request('POST', f'/tenants/{tenant_id}/connect/bluesky', json={
            'identifier': identifier,
            'appPassword': app_password
        })
        return _parse(TenantAccount, raw.get('data', raw))
    
    def connect_mastodon(
        self,
        tenant_id: str,
        instance_url: str,
        access_token: str
    ) -> TenantAccount:
        """Connect Mastodon account for tenant (token-based)"""
        raw = self._client._request('POST', f'/tenants/{tenant_id}/connect/mastodon', json={
            'instanceUrl': instance_url,
            'accessToken': access_token
        })
        return _parse(TenantAccount, raw.get('data', raw))
    
    def generate_client_token(
        self,
        tenant_id: str,
        components: Optional[List[str]] = None,
        expires_in: Optional[int] = None,
        allowed_origins: Optional[List[str]] = None
    ) -> ClientToken:
        """
        Generate a short-lived client token for embedding UI components.
        Use this token with the @schedulifyx/embed SDK on the frontend.
        
        Args:
            tenant_id: The tenant to generate a token for
            components: Which components to allow (default: all)
            expires_in: Token TTL in seconds (default: 3600, max: 3600)
            allowed_origins: Allowed origins for CORS (optional)
        
        Returns:
            ClientToken with token, expiresAt, components, origins, usage
        """
        data: Dict[str, Any] = {}
        if components:
            data['components'] = components
        if expires_in is not None:
            data['expiresIn'] = expires_in
        if allowed_origins:
            data['allowedOrigins'] = allowed_origins
        raw = self._client._request('POST', f'/tenants/{tenant_id}/client-token', json=data if data else None)
        return _parse(ClientToken, raw.get('data', raw))


class WebhooksAPI:
    """Webhooks API methods"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(self) -> List[Webhook]:
        """List all webhooks"""
        raw = self._client._request('GET', '/webhooks')
        return _parse_list(Webhook, raw.get('data', []))
    
    def get(self, webhook_id: str) -> Webhook:
        """Get a specific webhook"""
        raw = self._client._request('GET', f'/webhooks/{webhook_id}')
        return _parse(Webhook, raw.get('data', raw))
    
    def create(
        self,
        name: str,
        url: str,
        events: List[str],
        is_active: bool = True,
        retry_count: int = 3,
        timeout_seconds: int = 30
    ) -> Webhook:
        """Create a new webhook"""
        raw = self._client._request('POST', '/webhooks', json={
            'name': name,
            'url': url,
            'events': events,
            'isActive': is_active,
            'retryCount': retry_count,
            'timeoutSeconds': timeout_seconds
        })
        return _parse(Webhook, raw.get('data', raw))
    
    def update(
        self,
        webhook_id: str,
        name: Optional[str] = None,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
        retry_count: Optional[int] = None,
        timeout_seconds: Optional[int] = None
    ) -> Webhook:
        """Update a webhook"""
        data: Dict[str, Any] = {}
        if name is not None:
            data['name'] = name
        if url is not None:
            data['url'] = url
        if events is not None:
            data['events'] = events
        if is_active is not None:
            data['isActive'] = is_active
        if retry_count is not None:
            data['retryCount'] = retry_count
        if timeout_seconds is not None:
            data['timeoutSeconds'] = timeout_seconds
        raw = self._client._request('PATCH', f'/webhooks/{webhook_id}', json=data)
        return _parse(Webhook, raw.get('data', raw))
    
    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook"""
        return self._client._request('DELETE', f'/webhooks/{webhook_id}')
    
    def rotate_secret(self, webhook_id: str) -> Webhook:
        """Rotate webhook secret"""
        raw = self._client._request('POST', f'/webhooks/{webhook_id}/rotate-secret')
        return _parse(Webhook, raw.get('data', raw))
    
    def test(self, webhook_id: str, event_type: Optional[str] = None) -> Dict[str, Any]:
        """Test a webhook by sending a test event"""
        data: Dict[str, Any] = {}
        if event_type:
            data['eventType'] = event_type
        return self._client._request('POST', f'/webhooks/{webhook_id}/test', json=data)
    
    def get_events(
        self,
        webhook_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> PaginatedResponse:
        """Get webhook event history. Returns PaginatedResponse with data as list of WebhookEvent."""
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        raw = self._client._request('GET', f'/webhooks/{webhook_id}/events', params=params)
        items = _parse_list(WebhookEvent, raw.get('data', []))
        pagination = raw.get('pagination')
        return PaginatedResponse(data=items, pagination=pagination)
    
    def get_event_types(self) -> List[WebhookEventType]:
        """Get available event types"""
        raw = self._client._request('GET', '/webhooks/events/types')
        return _parse_list(WebhookEventType, raw.get('data', []))


class SchedulifyX:
    """
    SchedulifyX API Client v3.0 — Three-Tier Architecture
    
    Usage:
        client = SchedulifyX('sk_live_YOUR_API_KEY')
        
        # Tier 1: Tenants & Webhooks
        tenant = client.tenants.create(external_id='user_123', email='user@example.com')
        token = client.tenants.generate_client_token(tenant.id)
        
        # Tier 2: Publishing
        posts = client.posts.list()
        accounts = client.accounts.list()
        
        # Tier 3: Engagement
        comments = client.comments.list()
        conversations = client.inbox.list()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = 'https://api.schedulifyx.com',
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        })
        
        # Tier 1
        self.tenants = TenantsAPI(self)
        self.webhooks = WebhooksAPI(self)
        # Tier 2
        self.posts = PostsAPI(self)
        self.accounts = AccountsAPI(self)
        self.analytics = AnalyticsAPI(self)
        self.media = MediaAPI(self)
        self.queue = QueueAPI(self)
        self.profiles = ProfilesAPI(self)
        self.x = XTwitterAPI(self)
        # Tier 3
        self.comments = CommentsAPI(self)
        self.inbox = InboxAPI(self)
        self.mentions = MentionsAPI(self)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an API request"""
        url = f'{self.base_url}{endpoint}'
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=self.timeout
            )
            
            if not response.ok:
                try:
                    error_data = response.json() if response.text else {}
                    if isinstance(error_data, dict):
                        error = error_data.get('error', {})
                        if isinstance(error, dict):
                            raise SchedulifyXError(
                                message=error.get('message', f'HTTP {response.status_code}'),
                                code=error.get('code', 'http_error'),
                                status=response.status_code,
                                details=error.get('details')
                            )
                except (ValueError, AttributeError):
                    pass
                raise SchedulifyXError(
                    message=f'HTTP {response.status_code}',
                    code='http_error',
                    status=response.status_code,
                    details=None
                )
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise SchedulifyXError('Request timeout', 'timeout', 408)
        except requests.exceptions.ConnectionError as e:
            raise SchedulifyXError(str(e), 'network_error', 0)
    
    def usage(self) -> Usage:
        """Get API usage statistics"""
        raw = self._request('GET', '/usage')
        return _parse(Usage, raw.get('data', raw))


# ==================== TIER 2: POSTS ====================

class PostsAPI:
    """Posts API — Create, manage, and publish social media posts (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        status: Optional[str] = None,
        platform: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        tenant_user_id: Optional[str] = None
    ) -> PaginatedResponse:
        """List posts. Returns PaginatedResponse with data as list of Post."""
        params: Dict[str, Any] = {}
        if status:
            params['status'] = status
        if platform:
            params['platform'] = platform
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if tenant_user_id:
            params['tenantUserId'] = tenant_user_id
        raw = self._client._request('GET', '/posts', params=params)
        items = _parse_list(Post, raw.get('data', []))
        # Parse nested platforms in each post
        for i, item in enumerate(items):
            raw_post = raw.get('data', [])[i] if i < len(raw.get('data', [])) else {}
            if 'platforms' in raw_post:
                item.platforms = _parse_list(PostPlatform, raw_post['platforms'])
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def get(self, post_id: str) -> Post:
        """Get a single post"""
        raw = self._client._request('GET', f'/posts/{post_id}')
        post_data = raw.get('data', raw)
        post = _parse(Post, post_data)
        if 'platforms' in post_data:
            post.platforms = _parse_list(PostPlatform, post_data['platforms'])
        return post
    
    def create(
        self,
        platforms: List[Dict[str, Any]],
        content: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        tenant_user_id: Optional[str] = None,
        mode: Optional[str] = None  # 'publish' | 'schedule' | 'draft'
    ) -> Post:
        """Create a new post"""
        data: Dict[str, Any] = {'platforms': platforms}
        if content is not None:
            data['content'] = content
        if scheduled_for:
            data['scheduledFor'] = scheduled_for
        if media_urls:
            data['mediaUrls'] = media_urls
        if tenant_user_id:
            data['tenantUserId'] = tenant_user_id
        if mode:
            data['mode'] = mode
        raw = self._client._request('POST', '/posts', json=data)
        return _parse(Post, raw.get('data', raw))
    
    def update(
        self,
        post_id: str,
        content: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        status: Optional[str] = None
    ) -> Post:
        """Update a post (draft/scheduled only)"""
        data: Dict[str, Any] = {}
        if content is not None:
            data['content'] = content
        if scheduled_for:
            data['scheduledFor'] = scheduled_for
        if status:
            data['status'] = status
        raw = self._client._request('PATCH', f'/posts/{post_id}', json=data)
        return _parse(Post, raw.get('data', raw))
    
    def delete(self, post_id: str) -> Dict[str, Any]:
        """Delete a post (draft/scheduled only)"""
        return self._client._request('DELETE', f'/posts/{post_id}')
    
    def publish(self, post_id: str) -> Dict[str, Any]:
        """Publish a post immediately"""
        return self._client._request('POST', f'/posts/{post_id}/publish')


# ==================== TIER 2: ACCOUNTS ====================

class AccountsAPI:
    """Accounts API — List and inspect connected social accounts (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        platform: Optional[str] = None,
        active: Optional[bool] = None,
        tenant_user_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse:
        """List connected social accounts"""
        params: Dict[str, Any] = {}
        if platform:
            params['platform'] = platform
        if active is not None:
            params['active'] = active
        if tenant_user_id:
            params['tenantUserId'] = tenant_user_id
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        raw = self._client._request('GET', '/accounts', params=params)
        items = _parse_list(Account, raw.get('data', []))
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def get(self, account_id: str) -> AccountDetail:
        """Get account details"""
        raw = self._client._request('GET', f'/accounts/{account_id}')
        return _parse(AccountDetail, raw.get('data', raw))
    
    def get_pinterest_boards(self, account_id: str) -> Dict[str, Any]:
        """Get Pinterest boards for an account"""
        return self._client._request('GET', f'/accounts/{account_id}/pinterest-boards')


# ==================== TIER 2: ANALYTICS ====================

class AnalyticsAPI:
    """Analytics API — View analytics and engagement metrics (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def overview(self) -> AnalyticsOverview:
        """Get analytics overview"""
        raw = self._client._request('GET', '/analytics/overview')
        return _parse(AnalyticsOverview, raw.get('data', raw))
    
    def account(self, account_id: str, days: Optional[int] = None) -> List[AccountAnalyticsEntry]:
        """Get account analytics time series"""
        params: Dict[str, Any] = {}
        if days is not None:
            params['days'] = days
        raw = self._client._request('GET', f'/analytics/account/{account_id}', params=params)
        return _parse_list(AccountAnalyticsEntry, raw.get('data', []))
    
    def detailed(
        self,
        account_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> DetailedAnalytics:
        """Get detailed analytics"""
        params: Dict[str, Any] = {}
        if account_id:
            params['accountId'] = account_id
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date
        raw = self._client._request('GET', '/analytics', params=params)
        return _parse(DetailedAnalytics, raw.get('data', raw))


# ==================== TIER 2: MEDIA ====================

class MediaAPI:
    """Media API — Manage media library items (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        type: Optional[str] = None,
        folder: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse:
        """List media items"""
        params: Dict[str, Any] = {}
        if type:
            params['type'] = type
        if folder:
            params['folder'] = folder
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        raw = self._client._request('GET', '/media', params=params)
        items = _parse_list(MediaItem, raw.get('data', []))
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def get(self, media_id: str) -> MediaItem:
        """Get a single media item"""
        raw = self._client._request('GET', f'/media/{media_id}')
        return _parse(MediaItem, raw.get('data', raw))
    
    def upload(self, url: str, file_name: Optional[str] = None, folder: Optional[str] = None) -> MediaItem:
        """Upload media from URL"""
        data: Dict[str, Any] = {'url': url}
        if file_name:
            data['fileName'] = file_name
        if folder:
            data['folder'] = folder
        raw = self._client._request('POST', '/media', json=data)
        return _parse(MediaItem, raw.get('data', raw))


# ==================== TIER 2: QUEUE ====================

class QueueAPI:
    """Queue API — Manage posting queue schedules (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def get_slots(self, account_id: str) -> Dict[str, Any]:
        """Get queue schedule for an account"""
        return self._client._request('GET', '/queue/slots', params={'accountId': account_id})
    
    def set_slots(
        self,
        account_id: str,
        timezone: str,
        slots: List[Dict[str, Any]],
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Create or update queue schedule"""
        data: Dict[str, Any] = {
            'accountId': account_id,
            'timezone': timezone,
            'slots': slots
        }
        if is_active is not None:
            data['isActive'] = is_active
        return self._client._request('PUT', '/queue/slots', json=data)
    
    def delete_slots(self, account_id: str) -> Dict[str, Any]:
        """Delete queue schedule"""
        return self._client._request('DELETE', '/queue/slots', params={'accountId': account_id})
    
    def preview(self, account_id: str, count: Optional[int] = None) -> Dict[str, Any]:
        """Preview upcoming queue slots"""
        params: Dict[str, Any] = {'accountId': account_id}
        if count is not None:
            params['count'] = count
        return self._client._request('GET', '/queue/preview', params=params)
    
    def next_slot(self, account_id: str) -> Dict[str, Any]:
        """Get next available queue slot"""
        return self._client._request('GET', '/queue/next-slot', params={'accountId': account_id})
    
    def all(self) -> List[QueueSchedule]:
        """Get all queue schedules"""
        raw = self._client._request('GET', '/queue/all')
        return _parse_list(QueueSchedule, raw.get('data', []))


# ==================== TIER 2: PROFILES ====================

class ProfilesAPI:
    """Profiles API — Manage posting profiles/categories (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(self) -> List[Profile]:
        """List all profiles"""
        raw = self._client._request('GET', '/profiles')
        return _parse_list(Profile, raw.get('data', []))
    
    def get(self, profile_id: str) -> Profile:
        """Get a single profile"""
        raw = self._client._request('GET', f'/profiles/{profile_id}')
        return _parse(Profile, raw.get('data', raw))
    
    def create(self, name: str, description: Optional[str] = None, color: Optional[str] = None) -> Profile:
        """Create a new profile"""
        data: Dict[str, Any] = {'name': name}
        if description is not None:
            data['description'] = description
        if color:
            data['color'] = color
        raw = self._client._request('POST', '/profiles', json=data)
        return _parse(Profile, raw.get('data', raw))
    
    def update(self, profile_id: str, name: Optional[str] = None, description: Optional[str] = None, color: Optional[str] = None) -> Profile:
        """Update a profile"""
        data: Dict[str, Any] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if color:
            data['color'] = color
        raw = self._client._request('PUT', f'/profiles/{profile_id}', json=data)
        return _parse(Profile, raw.get('data', raw))
    
    def delete(self, profile_id: str) -> Dict[str, Any]:
        """Delete a profile"""
        return self._client._request('DELETE', f'/profiles/{profile_id}')


# ==================== TIER 2: X/TWITTER ====================

class XTwitterAPI:
    """X/Twitter API — Manage X/Twitter BYOK credentials and account modes (Tier 2)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def get_config(self) -> XConfig:
        """Get X/Twitter configuration"""
        raw = self._client._request('GET', '/x/config')
        return _parse(XConfig, raw.get('data', raw))
    
    def set_credentials(
        self,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str
    ) -> Dict[str, Any]:
        """Set BYOK (Bring Your Own Key) credentials"""
        return self._client._request('POST', '/x/credentials', json={
            'apiKey': api_key,
            'apiSecret': api_secret,
            'accessToken': access_token,
            'accessTokenSecret': access_token_secret
        })
    
    def set_mode(self, account_id: str, mode: str) -> Dict[str, Any]:
        """Switch X account mode ('byok' or 'wallet')"""
        return self._client._request('POST', '/x/mode', json={
            'accountId': account_id,
            'mode': mode
        })


# ==================== TIER 3: COMMENTS ====================

class CommentsAPI:
    """Comments API — Read and respond to social media comments (Tier 3)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        account_id: Optional[str] = None,
        post_id: Optional[str] = None,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        sentiment: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None  # 'newest' | 'oldest' | 'engagement'
    ) -> PaginatedResponse:
        """List comments"""
        params: Dict[str, Any] = {}
        if account_id:
            params['accountId'] = account_id
        if post_id:
            params['postId'] = post_id
        if platform:
            params['platform'] = platform
        if status:
            params['status'] = status
        if sentiment:
            params['sentiment'] = sentiment
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if sort_by:
            params['sortBy'] = sort_by
        raw = self._client._request('GET', '/comments', params=params)
        items = _parse_list(Comment, raw.get('data', []))
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def get(self, comment_id: str) -> Comment:
        """Get a single comment"""
        raw = self._client._request('GET', f'/comments/{comment_id}')
        return _parse(Comment, raw.get('data', raw))
    
    def get_replies(self, comment_id: str) -> List[Comment]:
        """Get replies to a comment"""
        raw = self._client._request('GET', f'/comments/{comment_id}/replies')
        return _parse_list(Comment, raw.get('data', []))
    
    def reply(self, comment_id: str, message: str) -> CommentReply:
        """Reply to a comment"""
        raw = self._client._request('POST', f'/comments/{comment_id}/reply', json={'message': message})
        return _parse(CommentReply, raw.get('data', raw))
    
    def stats(self) -> CommentStats:
        """Get comment statistics"""
        raw = self._client._request('GET', '/comments/stats/overview')
        return _parse(CommentStats, raw.get('data', raw))


# ==================== TIER 3: INBOX ====================

class InboxAPI:
    """Inbox API — Manage direct message conversations (Tier 3)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        account_id: Optional[str] = None,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        has_unread: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse:
        """List conversations"""
        params: Dict[str, Any] = {}
        if account_id:
            params['accountId'] = account_id
        if platform:
            params['platform'] = platform
        if status:
            params['status'] = status
        if has_unread is not None:
            params['hasUnread'] = has_unread
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        raw = self._client._request('GET', '/inbox/conversations', params=params)
        items = _parse_list(Conversation, raw.get('data', []))
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def get(self, conversation_id: str) -> Conversation:
        """Get a single conversation"""
        raw = self._client._request('GET', f'/inbox/conversations/{conversation_id}')
        return _parse(Conversation, raw.get('data', raw))
    
    def get_messages(
        self,
        conversation_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> PaginatedResponse:
        """Get messages in a conversation"""
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        raw = self._client._request('GET', f'/inbox/conversations/{conversation_id}/messages', params=params)
        items = _parse_list(Message, raw.get('data', []))
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def reply(self, conversation_id: str, message: str) -> Message:
        """Reply to a conversation"""
        raw = self._client._request('POST', f'/inbox/conversations/{conversation_id}/reply', json={'message': message})
        return _parse(Message, raw.get('data', raw))
    
    def stats(self) -> InboxStats:
        """Get inbox statistics"""
        raw = self._client._request('GET', '/inbox/stats')
        return _parse(InboxStats, raw.get('data', raw))


# ==================== TIER 3: MENTIONS ====================

class MentionsAPI:
    """Mentions API — Track brand mentions across platforms (Tier 3)"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        mention_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponse:
        """List mentions"""
        params: Dict[str, Any] = {}
        if platform:
            params['platform'] = platform
        if status:
            params['status'] = status
        if mention_type:
            params['mentionType'] = mention_type
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        raw = self._client._request('GET', '/mentions', params=params)
        items = _parse_list(Mention, raw.get('data', []))
        return PaginatedResponse(data=items, pagination=raw.get('pagination'))
    
    def stats(self) -> MentionStats:
        """Get mention statistics"""
        raw = self._client._request('GET', '/mentions/stats')
        return _parse(MentionStats, raw.get('data', raw))
