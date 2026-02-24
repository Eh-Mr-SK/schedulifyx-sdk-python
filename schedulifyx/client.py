"""
SchedulifyX API Client
"""

import requests
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlencode


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


class PostsAPI:
    """Posts API methods"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        status: Optional[str] = None,
        account_id: Optional[str] = None,
        platform: Optional[str] = None,
        tenant_user_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """List all posts with optional filters"""
        params = {}
        if status:
            params['status'] = status
        if account_id:
            params['accountId'] = account_id
        if platform:
            params['platform'] = platform
        if tenant_user_id:
            params['tenantUserId'] = tenant_user_id
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', '/posts', params=params)
    
    def get(self, post_id: str) -> Dict[str, Any]:
        """Get a single post by ID"""
        return self._client._request('GET', f'/posts/{post_id}')
    
    def create(
        self,
        content: str,
        platforms: List[Dict[str, str]],
        scheduled_for: Optional[str] = None,
        mode: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        tenant_user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new post"""
        data: Dict[str, Any] = {
            'content': content,
            'platforms': platforms,
        }
        if scheduled_for:
            data['scheduledFor'] = scheduled_for
        if mode:
            data['mode'] = mode
        if media_urls:
            data['mediaUrls'] = media_urls
        if tenant_user_id:
            data['tenantUserId'] = tenant_user_id
        return self._client._request('POST', '/posts', json=data)
    
    def update(
        self,
        post_id: str,
        content: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing post"""
        data: Dict[str, Any] = {}
        if content is not None:
            data['content'] = content
        if scheduled_for is not None:
            data['scheduledFor'] = scheduled_for
        if status is not None:
            data['status'] = status
        return self._client._request('PATCH', f'/posts/{post_id}', json=data)
    
    def delete(self, post_id: str) -> Dict[str, Any]:
        """Delete a post"""
        return self._client._request('DELETE', f'/posts/{post_id}')
    
    def publish(self, post_id: str) -> Dict[str, Any]:
        """Publish a post immediately"""
        return self._client._request('POST', f'/posts/{post_id}/publish')


class AccountsAPI:
    """Accounts API methods"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        platform: Optional[str] = None,
        active: Optional[bool] = None,
        tenant_user_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """List all connected social accounts"""
        params = {}
        if platform:
            params['platform'] = platform
        if active is not None:
            params['active'] = str(active).lower()
        if tenant_user_id:
            params['tenantUserId'] = tenant_user_id
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', '/accounts', params=params)
    
    def get(self, account_id: str) -> Dict[str, Any]:
        """Get a single account by ID"""
        return self._client._request('GET', f'/accounts/{account_id}')
    
    def get_pinterest_boards(self, account_id: str) -> Dict[str, Any]:
        """Get Pinterest boards for a Pinterest account"""
        return self._client._request('GET', f'/accounts/{account_id}/pinterest-boards')


class AnalyticsAPI:
    """Analytics API methods"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def overview(self) -> Dict[str, Any]:
        """Get analytics overview"""
        return self._client._request('GET', '/analytics/overview')
    
    def for_account(self, account_id: str, days: Optional[int] = None) -> Dict[str, Any]:
        """Get analytics for a specific account"""
        params = {}
        if days:
            params['days'] = days
        return self._client._request('GET', f'/analytics/account/{account_id}', params=params)
    
    def list(
        self,
        account_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get all analytics data"""
        params = {}
        if account_id:
            params['accountId'] = account_id
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date
        return self._client._request('GET', '/analytics', params=params)


class ProfilesAPI:
    """Profiles API methods"""

    def __init__(self, client: 'SchedulifyX'):
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all publishing profiles"""
        return self._client._request('GET', '/profiles')

    def get(self, profile_id: str) -> Dict[str, Any]:
        """Get a single profile by ID"""
        return self._client._request('GET', f'/profiles/{profile_id}')

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        color: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new publishing profile"""
        data: Dict[str, Any] = {'name': name}
        if description:
            data['description'] = description
        if color:
            data['color'] = color
        return self._client._request('POST', '/profiles', json=data)

    def update(
        self,
        profile_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing profile"""
        data: Dict[str, Any] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if color is not None:
            data['color'] = color
        return self._client._request('PUT', f'/profiles/{profile_id}', json=data)

    def delete(self, profile_id: str) -> Dict[str, Any]:
        """Delete a profile"""
        return self._client._request('DELETE', f'/profiles/{profile_id}')


class QueueAPI:
    """Queue API methods"""
    
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
        is_active: bool = True
    ) -> Dict[str, Any]:
        """Create or update queue schedule"""
        return self._client._request('PUT', '/queue/slots', json={
            'accountId': account_id,
            'timezone': timezone,
            'slots': slots,
            'isActive': is_active
        })
    
    def delete_slots(self, account_id: str) -> Dict[str, Any]:
        """Delete queue schedule"""
        return self._client._request('DELETE', '/queue/slots', params={'accountId': account_id})
    
    def get_next_slot(self, account_id: str) -> Dict[str, Any]:
        """Get the next available slot"""
        return self._client._request('GET', '/queue/next-slot', params={'accountId': account_id})
    
    def preview(self, account_id: str, count: Optional[int] = None) -> Dict[str, Any]:
        """Preview upcoming slots"""
        params = {'accountId': account_id}
        if count:
            params['count'] = count
        return self._client._request('GET', '/queue/preview', params=params)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all queue schedules"""
        return self._client._request('GET', '/queue/all')


class WebhooksAPI:
    """Webhooks API methods"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(self) -> Dict[str, Any]:
        """List all webhooks"""
        return self._client._request('GET', '/webhooks')
    
    def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a specific webhook"""
        return self._client._request('GET', f'/webhooks/{webhook_id}')
    
    def create(
        self,
        name: str,
        url: str,
        events: List[str],
        is_active: bool = True,
        retry_count: int = 3,
        timeout_seconds: int = 30
    ) -> Dict[str, Any]:
        """Create a new webhook"""
        return self._client._request('POST', '/webhooks', json={
            'name': name,
            'url': url,
            'events': events,
            'isActive': is_active,
            'retryCount': retry_count,
            'timeoutSeconds': timeout_seconds
        })
    
    def update(
        self,
        webhook_id: str,
        name: Optional[str] = None,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
        retry_count: Optional[int] = None,
        timeout_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update a webhook"""
        data = {}
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
        return self._client._request('PATCH', f'/webhooks/{webhook_id}', json=data)
    
    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook"""
        return self._client._request('DELETE', f'/webhooks/{webhook_id}')
    
    def rotate_secret(self, webhook_id: str) -> Dict[str, Any]:
        """Rotate webhook secret"""
        return self._client._request('POST', f'/webhooks/{webhook_id}/rotate-secret')
    
    def test(self, webhook_id: str, event_type: Optional[str] = None) -> Dict[str, Any]:
        """Test a webhook by sending a test event"""
        data = {}
        if event_type:
            data['eventType'] = event_type
        return self._client._request('POST', f'/webhooks/{webhook_id}/test', json=data)
    
    def get_events(
        self,
        webhook_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get webhook event history"""
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', f'/webhooks/{webhook_id}/events', params=params)
    
    def get_event_types(self) -> Dict[str, Any]:
        """Get available event types"""
        return self._client._request('GET', '/webhooks/events/types')


class TenantsAPI:
    """Tenants API methods for multi-tenant integrations"""
    
    def __init__(self, client: 'SchedulifyX'):
        self._client = client
    
    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """List all tenants"""
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        if search:
            params['search'] = search
        return self._client._request('GET', '/tenants', params=params)
    
    def get(self, tenant_id: str) -> Dict[str, Any]:
        """Get a single tenant"""
        return self._client._request('GET', f'/tenants/{tenant_id}')
    
    def create(
        self,
        external_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new tenant"""
        data = {'externalId': external_id}
        if email:
            data['email'] = email
        if name:
            data['name'] = name
        if metadata:
            data['metadata'] = metadata
        return self._client._request('POST', '/tenants', json=data)
    
    def update(
        self,
        tenant_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update a tenant"""
        data = {}
        if email is not None:
            data['email'] = email
        if name is not None:
            data['name'] = name
        if metadata is not None:
            data['metadata'] = metadata
        if is_active is not None:
            data['isActive'] = is_active
        return self._client._request('PATCH', f'/tenants/{tenant_id}', json=data)
    
    def delete(self, tenant_id: str) -> Dict[str, Any]:
        """Delete a tenant"""
        return self._client._request('DELETE', f'/tenants/{tenant_id}')
    
    def get_connect_url(self, tenant_id: str, platform: str, redirect_uri: Optional[str] = None) -> Dict[str, Any]:
        """Get OAuth URL for tenant to connect a platform"""
        params = {}
        if redirect_uri:
            params['redirectUri'] = redirect_uri
        return self._client._request('GET', f'/tenants/{tenant_id}/connect/{platform}', params=params if params else None)
    
    def list_accounts(self, tenant_id: str) -> Dict[str, Any]:
        """List tenant's connected accounts"""
        return self._client._request('GET', f'/tenants/{tenant_id}/accounts')
    
    def disconnect_account(self, tenant_id: str, account_id: str) -> Dict[str, Any]:
        """Disconnect a tenant's account"""
        return self._client._request('DELETE', f'/tenants/{tenant_id}/accounts/{account_id}')
    
    def connect_bluesky(
        self,
        tenant_id: str,
        identifier: str,
        app_password: str
    ) -> Dict[str, Any]:
        """Connect Bluesky account for tenant"""
        return self._client._request('POST', f'/tenants/{tenant_id}/connect/bluesky', json={
            'identifier': identifier,
            'appPassword': app_password
        })
    
    def connect_mastodon(
        self,
        tenant_id: str,
        instance_url: str,
        access_token: str
    ) -> Dict[str, Any]:
        """Connect Mastodon account for tenant"""
        return self._client._request('POST', f'/tenants/{tenant_id}/connect/mastodon', json={
            'instanceUrl': instance_url,
            'accessToken': access_token
        })


class CommentsAPI:
    """Comments API methods"""

    def __init__(self, client: 'SchedulifyX'):
        self._client = client

    def list(
        self,
        account_id: Optional[str] = None,
        platform: Optional[str] = None,
        post_id: Optional[str] = None,
        status: Optional[str] = None,
        sentiment: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List comments across all accounts"""
        params: Dict[str, Any] = {}
        if account_id:
            params['accountId'] = account_id
        if platform:
            params['platform'] = platform
        if post_id:
            params['postId'] = post_id
        if status:
            params['status'] = status
        if sentiment:
            params['sentiment'] = sentiment
        if sort_by:
            params['sortBy'] = sort_by
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', '/comments', params=params)

    def get(self, comment_id: str) -> Dict[str, Any]:
        """Get a single comment by ID"""
        return self._client._request('GET', f'/comments/{comment_id}')

    def get_replies(self, comment_id: str) -> Dict[str, Any]:
        """Get replies to a comment"""
        return self._client._request('GET', f'/comments/{comment_id}/replies')

    def reply(self, comment_id: str, message: str) -> Dict[str, Any]:
        """Reply to a comment"""
        return self._client._request('POST', f'/comments/{comment_id}/reply', json={
            'message': message
        })

    def stats(self) -> Dict[str, Any]:
        """Get comment statistics overview"""
        return self._client._request('GET', '/comments/stats/overview')


class InboxAPI:
    """Inbox / Conversations API methods"""

    def __init__(self, client: 'SchedulifyX'):
        self._client = client

    def list(
        self,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        has_unread: Optional[bool] = None,
        account_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List conversations"""
        params: Dict[str, Any] = {}
        if platform:
            params['platform'] = platform
        if status:
            params['status'] = status
        if has_unread is not None:
            params['hasUnread'] = str(has_unread).lower()
        if account_id:
            params['accountId'] = account_id
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', '/inbox/conversations', params=params)

    def get(self, conversation_id: str) -> Dict[str, Any]:
        """Get a specific conversation"""
        return self._client._request('GET', f'/inbox/conversations/{conversation_id}')

    def get_messages(
        self,
        conversation_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get messages in a conversation"""
        params: Dict[str, Any] = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', f'/inbox/conversations/{conversation_id}/messages', params=params)

    def reply(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Send a reply in a conversation"""
        return self._client._request('POST', f'/inbox/conversations/{conversation_id}/reply', json={
            'message': message
        })

    def stats(self) -> Dict[str, Any]:
        """Get inbox statistics"""
        return self._client._request('GET', '/inbox/stats')


class MentionsAPI:
    """Mentions API methods"""

    def __init__(self, client: 'SchedulifyX'):
        self._client = client

    def list(
        self,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        mention_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List mentions across platforms"""
        params: Dict[str, Any] = {}
        if platform:
            params['platform'] = platform
        if status:
            params['status'] = status
        if mention_type:
            params['mentionType'] = mention_type
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._client._request('GET', '/mentions', params=params)

    def stats(self) -> Dict[str, Any]:
        """Get mention statistics"""
        return self._client._request('GET', '/mentions/stats')


class XTwitterAPI:
    """X/Twitter BYOK API methods"""

    def __init__(self, client: 'SchedulifyX'):
        self._client = client

    def get_config(self) -> Dict[str, Any]:
        """Get X/Twitter BYOK configuration and account modes"""
        return self._client._request('GET', '/x/config')

    def set_credentials(
        self,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> Dict[str, Any]:
        """Set X/Twitter BYOK API credentials"""
        return self._client._request('POST', '/x/credentials', json={
            'apiKey': api_key,
            'apiSecret': api_secret,
            'accessToken': access_token,
            'accessTokenSecret': access_token_secret,
        })

    def switch_mode(self, account_id: str, mode: str) -> Dict[str, Any]:
        """Switch X/Twitter mode for an account ('byok' or 'wallet')"""
        return self._client._request('POST', '/x/mode', json={
            'accountId': account_id,
            'mode': mode,
        })


class SchedulifyX:
    """
    SchedulifyX API Client
    
    Usage:
        client = SchedulifyX('sk_live_YOUR_API_KEY')
        posts = client.posts.list()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = 'https://api.schedulifyx.com',
        timeout: int = 30
    ):
        """
        Initialize the SchedulifyX client.
        
        Args:
            api_key: Your SchedulifyX API key
            base_url: API base URL (default: https://api.schedulifyx.com)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        })
        
        # Initialize API namespaces
        self.posts = PostsAPI(self)
        self.accounts = AccountsAPI(self)
        self.analytics = AnalyticsAPI(self)
        self.profiles = ProfilesAPI(self)
        self.queue = QueueAPI(self)
        self.webhooks = WebhooksAPI(self)
        self.tenants = TenantsAPI(self)
        self.comments = CommentsAPI(self)
        self.inbox = InboxAPI(self)
        self.mentions = MentionsAPI(self)
        self.x_twitter = XTwitterAPI(self)
    
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
    
    def usage(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        return self._request('GET', '/usage')
