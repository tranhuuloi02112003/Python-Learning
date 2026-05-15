from django.views.generic import TemplateView

from .selectors import get_dashboard_summary


class DashboardView(TemplateView):
    # TemplateView dùng cho những page chủ yếu chỉ render template.
    template_name = "dashboard/index.html"

    # Thêm dữ liệu vào context trước khi render dashboard/index.html.
    def get_context_data(self, **kwargs):
        # Lấy context mặc định từ TemplateView trước, rồi bổ sung data riêng.
        context = super().get_context_data(**kwargs)
        context.update(get_dashboard_summary())
        context["active_nav"] = "dashboard"
        return context
