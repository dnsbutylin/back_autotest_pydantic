// Читает данные ИП
// С сайта https://www.rusprofile.ru/search?query=%D0%98%D0%9F%20%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2&search_inactive=2&type=ip

let items = document.querySelectorAll(".company-item");
let data = [];
for (let item of items) {
    let ip = {}
    ip.name = item.querySelector('.company-item__title').textContent.trim();
    for (let field of item.querySelectorAll('.company-item-info > dl')) {
        let key = field.querySelector('dt').textContent.toUpperCase().trim();
        ip[key] = field.querySelector('dd').textContent.trim();
    }
    data.push(ip);
}
console.log(JSON.stringify(data));
