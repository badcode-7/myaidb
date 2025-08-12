// 获取token
const token = localStorage.getItem('token');

// 检查登录状态
if (!token) {
    window.location.href = '/';
}

// 加载用户数据
async function loadUserProfile() {
    try {
        const response = await fetch('/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('获取用户信息失败');
        }
        
        const user = await response.json();
        renderUserProfile(user);
    } catch (error) {
        alert(error.message);
        window.location.href = '/';
    }
}

// 渲染用户信息
function renderUserProfile(user) {
    document.getElementById('username').textContent = user.username;
    document.getElementById('email').textContent = user.email;
    document.getElementById('vipStatus').textContent = user.is_vip ? 'VIP会员' : '普通会员';
    
    // 格式化日期
    const createdAt = new Date(user.created_at);
    document.getElementById('createdAt').textContent = createdAt.toLocaleString();
}

// 登出功能
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '/';
});

// 页面加载时获取用户数据
loadUserProfile();
