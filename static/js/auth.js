// 登录表单处理
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '登录失败');
        }
        
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        
        // 检查是否是管理员
        const tokenPayload = JSON.parse(atob(data.access_token.split('.')[1]));
        if (tokenPayload.is_admin) {
            window.location.href = '/admin.html';
        } else {
            window.location.href = '/profile.html';
        }
    } catch (error) {
        alert(error.message);
    }
});

// 注册表单处理
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                password
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '注册失败');
        }
        
        alert('注册成功，请登录');
        document.getElementById('login-tab').click();
    } catch (error) {
        alert(error.message);
    }
});

// 检查是否已登录
function checkAuth() {
    const token = localStorage.getItem('token');
    if (token) {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        if (tokenPayload.is_admin) {
            window.location.href = '/admin.html';
        } else {
            window.location.href = '/profile.html';
        }
    }
}

// 页面加载时检查登录状态
checkAuth();
