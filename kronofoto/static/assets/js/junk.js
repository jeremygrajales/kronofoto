const toggleVis = evt => {
    const el = document.querySelector('#metadata')
    if (!el.classList.replace('hidden', 'gridden')) {
        el.classList.replace('gridden', 'hidden')
    }
}
const forward = document.getElementById('forward')
const carousel = document.getElementById('fi-thumbnail-carousel-images')

const mouseDown = () => {
}

const delay = ms => new Promise((resolve, reject) => setTimeout(resolve, ms))

const mouseUp = () => new Promise((resolve, reject) => 
    forward.addEventListener("mouseup", resolve, {once: true})
)

const animationEnd = element => new Promise((resolve, reject) => 
    element.addEventListener('animationend', resolve, {once: true})
)

const request = (verb, resource) => new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open(verb, resource)
    xhr.onload = () => {
        if (xhr.status === 200) {
            resolve(JSON.parse(xhr.responseText))
        } else {
            reject(`${verb} ${resource} returned ${xhr.status}`)
        }
    }
    xhr.send()
})

const loadstate = data => {
    current_state = data
    carousel.setAttribute('style', 'animation: none')
    carousel.innerHTML = data.thumbnails
    document.getElementById('fi-image').setAttribute('src', data.h700)
    forward_json = data.forward.json_url
}

let current_state = JSON.parse(document.getElementById('initial-state').textContent)
window.history.replaceState(current_state, 'Fortepan Iowa', current_state.url)
    
window.onpopstate = evt => {
    loadstate(evt.state)
}

const scrollAction = (evt) => {
    const next_page = request('GET', current_state.forward.json_url)
    let p
    if (evt.event === 'click') {
        p = Promise.resolve(evt)
    } else if (evt.event === 'startScroll') {
        const scrollEnd = animationEnd(carousel)
        void carousel.offsetWidth
        carousel.setAttribute('style', 'animation: from-100-to-200 10s linear;')
        p = Promise.race([
            mouseUp().then(() => ({event: 'click', position: Math.round(-100 - (new Date() - evt.begin)/100)})),
            scrollEnd.then(() => ({event: 'startScroll', begin: new Date()})),
        ])
    }
    const scroll2end = p.then(evt => {
        if (evt.event === 'click') {
            document.getElementById('fi-image').setAttribute('src', current_state.forward.h700)
            carousel.setAttribute('style', `animation: from${evt.position}-to-200 500ms ease-out;`)
            return animationEnd(carousel)
        } 
        return evt
    })
    Promise.all([next_page, scroll2end]).then(([data, evt]) => {
        loadstate(data)
        window.history.pushState(data, 'Fortepan Iowa', data.url)
        if (evt.event === 'startScroll') {
            scrollAction(evt)
        }
    })
}

forward.addEventListener("mousedown", () => 
    Promise.race([
        mouseUp().then(() => ({event: 'click', position: -100})),
        delay(500).then(() => ({event: 'startScroll', begin: new Date()}))
    ]).then(scrollAction))

const forward_click = () => {
    return false;
}

