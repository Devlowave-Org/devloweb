window.addEventListener("scroll", () => {
  let e = 0;
  scrollY >= 83 && scrollY <= 800
    ? document
        .querySelector(".end-header")
        .querySelectorAll(".section-items")
        .forEach((t) => {
          setTimeout(() => {
            t.classList.add("end-header-animation");
          }, e),
            (e += 200);
        })
    : scrollY >= 1100 && scrollY <= 1900
    ? (document.querySelectorAll(".second-section-1-item").forEach((t) => {
        setTimeout(() => {
          t.classList.add("second-section-item-animation");
        }, e),
          (e += 300);
      }),
      scrollY >= 1200 &&
        scrollY <= 1700 &&
        document
          .querySelector(".second-section-1-container")
          .querySelector(".left")
          .querySelector("h3")
          .classList.add("second-section-h3-animation"))
    : scrollY >= 1800 && scrollY <= 2550
    ? (document.querySelectorAll(".little-image-container").forEach((e) => {
        e.classList.add("little-image-container-animation");
      }),
      document.querySelector(".middle").classList.add("middle-animation"),
      scrollY >= 2e3 &&
        (document
          .querySelector(".arrow-left")
          .classList.add("arrow-left-animation"),
        document
          .querySelector(".arrow-right")
          .classList.add("arrow-right-animation")))
    : scrollY >= 2400 &&
      scrollY <= 2700 &&
      (document
        .querySelector("#instagram-section")
        .querySelector(".img-container")
        .classList.add("instagram-img-container"),
      document
        .querySelector("#instagram-section")
        .querySelector(".imgs-container")
        .querySelectorAll(".img-container")
        .forEach((e) => {
          e.classList.add("instagram-img-container");
        }));
}),
  window.addEventListener("load", () => {
    document
      .querySelector("#navbar-desktop")
      ?.classList.add("navbar-animation"),
      document
        .querySelector("#navbar-mobile")
        ?.classList.add("navbar-animation"),
      document
        .querySelector(".header-image")
        .classList.add("header-image-animation"),
      document
        .querySelector(".header-text-information")
        .classList.add("header-text-animation");
  });
const burger = document
    .querySelector("#navbar-mobile")
    .querySelector(".burger-menu"),
  cross = document.querySelector(".cross");
burger.addEventListener("click", () => {
  document
    .querySelector("#navbar-mobile")
    .querySelector(".onglet-container")
    .classList.add("onglet-container-active");
}),
  cross.addEventListener("click", () => {
    document
      .querySelector("#navbar-mobile")
      .querySelector(".onglet-container")
      .classList.remove("onglet-container-active");
  });

const form = document.querySelector("form"),
  email = document.querySelector("#email"),
  message = document.querySelector("#text"),
  labelEmail = document.querySelector(".label-email"),
  labelMessage = document.querySelector(".label-text"),
  button = document.querySelector(".button-form");
let userEmail = "",
  isPass = !1;
console.log(message),
  form.addEventListener("submit", (e) => {
    if ((e.preventDefault(), isPass)) {
      if ("" === message.value) return;
      console.log(message.value),
        (window.location.href = `mailto:${userEmail}?subject=${encodeURIComponent(
          "Message provenant du site."
        )}&body=${encodeURIComponent(message.value)}`);
    }
    "" !== email.value &&
      ((userEmail = email.value),
      (labelEmail.style.display = "none"),
      (labelMessage.style.display = "block"),
      (button.innerText = "Envoyer !"),
      (isPass = !0),
      window.innerWidth <= 720 &&
        ((form.style.flexDirection = "column"),
        (button.style.width = "100%"),
        (message.style.minHeight = "300px")));
  });
