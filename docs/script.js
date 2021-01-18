let sys = document.getElementsByClassName("system")
let debug = document.getElementById("debug")

console.log(sys)
let hideDebug = false;

function applyDebugStyle() {
  let style = document.createElement('style');

  if (hideDebug) {
    debug.innerHTML = "Show debug 😛"
    for (i=0; i < sys.length; i++){
    sys[i].style.display = "none"
  }

  } else {
    debug.innerHTML = "Hide debug 🥵"
    for (i=0; i < sys.length; i++){
      sys[i].style.display = "block"
    }
  } 
}

debug.addEventListener("click", () => {
  hideDebug = !hideDebug;
  applyDebugStyle()
})