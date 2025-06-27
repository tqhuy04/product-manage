// ✅ public/js/login.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const googleLoginBtn = document.getElementById("google-login");
    const facebookLoginBtn = document.getElementById("facebook-login");

    //  Xử lý đăng nhập bằng username/password
    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(form);
            const username = formData.get("username").trim();
            const password = formData.get("password");

            try {
                const response = await fetch("/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: new URLSearchParams({
                        username,
                        password,
                    }),
                });

                const result = await response.json();

                if (response.ok) {
                    localStorage.setItem("token", result.access_token);
                    alert("🎉 Đăng nhập thành công!");
                    window.location.href = "/sendemail.html";
                } else {
                    alert("❌ " + (result.detail || "Đăng nhập thất bại"));
                }
            } catch (error) {
                console.error("⚠️ Lỗi:", error);
                alert("Không thể kết nối đến máy chủ.");
            }
        });
    }

    // Xử lý nút đăng nhập bằng Google
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener("click", () => {
            window.location.href = "/auth/google-login";
        });
    }
    if (facebookLoginBtn) {
    facebookLoginBtn.addEventListener("click", () => {
        window.location.href = "/auth/facebook-login";
    });
}
});
