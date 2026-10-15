const form = document.getElementById('form');

if (form) {
  form.addEventListener('submit', e => {
    // clientside validation is done by html5 form validate tags!
    // e.preventDefault();
  });
}

const addToCarts = document.querySelectorAll('[data-action=addtocart]')

addToCarts.forEach(element => {
  element.addEventListener('click', e => {
    e.preventDefault()
    fetch(`addtocart?product_id=${element.getAttribute('data-id')}`).then(res => {
      if (res.redirected) {
        window.location = res.url
        return
      }
      return res.json()
    }).then(json => {
      if (json.error) {
        window.alert(json.error)
        return
      }
      window.alert(json.msg)
      const iv = element.closest('.card').querySelector('#iv')
      iv.textContent = Number(iv.textContent) - 1
    })
  })
})