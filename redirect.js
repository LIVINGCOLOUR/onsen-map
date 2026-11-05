// 旧URL（namaonsen.mon-m.workers.dev）へのアクセスを、新しい kakeyu.pages.dev へ移す。
export default {
  fetch(request) {
    const u = new URL(request.url);
    return Response.redirect("https://kakeyu.pages.dev" + u.pathname + u.search, 301);
  },
};
