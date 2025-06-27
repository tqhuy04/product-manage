// ✅ public/js/register.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");

    if (!form) {
        console.error("Không tìm thấy form với id 'register-form'");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const username = form.querySelector("input[name='username']").value.trim();
        const email = form.querySelector("input[name='email']").value.trim();
        const password = form.querySelector("input[name='password']").value;

        try {
            const response = await fetch("/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("🎉 Đăng ký thành công!");
                window.location.href = "/login.html"; // ❗ bạn đang mount /public làm root
            } else {
                alert("❌ Lỗi đăng ký: " + (data.detail || "Không rõ nguyên nhân"));
            }
        } catch (err) {
            console.error("⚠️ Lỗi kết nối:", err);
            alert("Không thể kết nối đến máy chủ.");
        }
    });
});
