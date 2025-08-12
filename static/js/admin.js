// 获取token
const token = localStorage.getItem('token');

// 检查登录状态和权限
if (!token) {
    window.location.href = '/';
} else {
    const payload = JSON.parse(atob(token.split('.')[1]));
    if (!payload.is_admin) {
        window.location.href = '/profile.html';
    }
}

// 加载用户数据
async function loadUsers() {
    try {
        const response = await fetch('/admin/users', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('获取用户数据失败');
        }
        
        const users = await response.json();
        renderUsers(users);
    } catch (error) {
        alert(error.message);
    }
}

// 渲染用户列表
function renderUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';
    
    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.id}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>
                <div class="form-check form-switch">
                    <input class="form-check-input vip-switch" type="checkbox" 
                        ${user.is_vip ? 'checked' : ''} 
                        data-user-id="${user.id}">
                </div>
            </td>
            <td>${user.is_admin ? '是' : '否'}</td>
            <td>
                <button class="btn btn-danger btn-sm delete-btn" 
                    data-user-id="${user.id}">删除</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    // 添加VIP切换事件
    document.querySelectorAll('.vip-switch').forEach(switchEl => {
        switchEl.addEventListener('change', handleVipChange);
    });
    
    // 添加删除按钮事件
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', handleDeleteUser);
    });
}

// 处理VIP状态变更
async function handleVipChange(e) {
    const userId = e.target.dataset.userId;
    const isVip = e.target.checked;
    
    try {
        const response = await fetch(`/users/${userId}/vip`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                is_vip: isVip
            })
        });
        
        if (!response.ok) {
            throw new Error('更新VIP状态失败');
        }
        
        alert('VIP状态已更新');
    } catch (error) {
        alert(error.message);
        e.target.checked = !isVip; // 恢复之前的状态
    }
}

// 处理删除用户
async function handleDeleteUser(e) {
    if (!confirm('确定要删除此用户吗？')) return;
    
    const userId = e.target.dataset.userId;
    
    try {
        const response = await fetch(`/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('删除用户失败');
        }
        
        alert('用户已删除');
        loadUsers(); // 刷新列表
    } catch (error) {
        alert(error.message);
    }
}

// 登出功能
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '/';
});

// 页面加载时获取用户数据
loadUsers();
