import Vue from "vue";
import * as Components from "./components/**/*.vue";

Object.values(Components).map(a => a.name && Vue.component(a.name, a));
const selector = new Vue({ render: h => h("Selector") });

if (document.getElementById("vue-selector") != null) {
  selector.$mount("vue-selector");
}
