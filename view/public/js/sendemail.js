document.addEventListener("DOMContentLoaded", async () => {
    // Bước 1: Lấy token từ URL (nếu có) và lưu vào localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const urlToken = urlParams.get("token");
    if (urlToken) {
        localStorage.setItem("token", urlToken);
        // Xóa token khỏi URL để gọn gàng
        window.history.replaceState({}, document.title, "/sendemail.html");
    }

    // Bước 2: Lấy token từ localStorage
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Vui lòng đăng nhập trước.");
        window.location.href = "/login.html";
        return;
    }

    // Bước 3: Giải mã token để lấy username
    let username = "";
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        username = payload.sub;
    } catch (e) {
        alert("Token không hợp lệ, vui lòng đăng nhập lại.");
        localStorage.removeItem("token");
        window.location.href = "/login.html";
        return;
    }

    // Gợi ý subject
    const subjectField = document.getElementById("subject");
    if (subjectField) {
        subjectField.value = `Thư từ hệ thống của ${username}`;
    }

    const form = document.getElementById("emailForm");
    if (!form) {
        alert("Không tìm thấy form gửi email.");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const to = document.getElementById("to").value;
        const subject = document.getElementById("subject").value;
        const body = document.getElementById("body").value;

        try {
            const res = await fetch("/email/send_invite", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ to, subject, body })
            });

            const result = await res.json();
            if (res.ok) {
                alert(result.result || "📧 Email đã được gửi thành công!");
                form.reset();
            } else {
                alert("Lỗi gửi email: " + (result.detail || "Không rõ nguyên nhân"));
            }
        } catch (err) {
            console.error("Lỗi:", err);
            alert("Gửi email thất bại do lỗi hệ thống.");
        }
    });
});
