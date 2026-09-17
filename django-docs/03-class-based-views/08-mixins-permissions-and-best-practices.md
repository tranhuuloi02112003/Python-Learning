# 08. Mixins, Permissions và Best Practices

> ⚠️ **Bài này chưa được viết.** File giữ chỗ để không gãy thứ tự đọc.

Nội dung dự kiến:

- `LoginRequiredMixin`, `PermissionRequiredMixin`, `UserPassesTestMixin`
- Thứ tự kế thừa mixin (mixin đứng trước class view, vì sao)
- Tự viết mixin dùng chung cho nhiều view
- Best practices: khi nào override `get_queryset()` thay vì `get_context_data()`,
  tránh nhét business logic vào view

Trong lúc chờ, phần permission ở tầng API được giải thích tại
`../05-drf-roadmap/focus/10-authentication-permission-basic.md`.

---

**Điều hướng:** ← `07-formview-and-form-handling.md` · `00-lo-trinh-doc.md` · →
