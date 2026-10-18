// Preserve old WordPress page-ID links when visitors follow bookmarks.
(() => {
  const paths = {8: '/', 12: '/publications/', 20: '/contact/', 66: '/'};
  const id = new URLSearchParams(location.search).get('page_id');
  if (Object.hasOwn(paths, id)) {
    const base = document.currentScript.dataset.basePath || '';
    location.replace(base + paths[id] + location.hash);
  }
})();
