(window.webpackJsonp=window.webpackJsonp||[]).push([[19],{699:function(e,t,n){var content=n(729);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(93).default)("4ee98e4a",content,!0,{sourceMap:!1})},713:function(e,t,n){"use strict";n.r(t);n(81),n(95),n(404);var o={model:{prop:"areChecked",event:"change"},props:["areChecked","value","id","disabled","label","allowMultiple"],data:function(){return{checked:this.value||!1}},computed:{classes:function(){return{active:Array.isArray(this.areChecked)?this.areChecked.includes(this.value):this.checked,disabled:this.disabled}}},watch:{value:function(){this.checked=!!this.value}},methods:{toggleCheck:function(){if(!this.disabled){var e=this.areChecked,t=e.indexOf(this.value);t>=0?e.splice(t,1):(e.length&&!this.allowMultiple&&(e=[]),e.push(this.value)),this.$emit("change",e)}}}},r=(n(728),n(50)),component=Object(r.a)(o,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"re-annotation-button",class:[e.classes,e.allowMultiple?"multiple":"single"]},[n("label",{staticClass:"button",attrs:{for:e.id},on:{click:function(t){return t.preventDefault(),e.toggleCheck.apply(null,arguments)}}},[n("span",{staticClass:"annotation-button-data__text",attrs:{title:e.label.class}},[e._v(e._s(e.label.class)+"\n    ")]),e._v(" "),e.label.score>0?n("div",{staticClass:"annotation-button-data__info"},[n("span",[e._v(e._s(e._f("percent")(e.label.score)))])]):e._e()]),e._v(" "),n("div",{staticClass:"annotation-button-container",attrs:{tabindex:"0"},on:{click:function(t){return t.stopPropagation(),e.toggleCheck.apply(null,arguments)}}},[n("input",{attrs:{id:e.id,type:"checkbox",disabled:e.disabled},domProps:{value:e.value,checked:e.checked}})])])}),[],!1,null,"b966c16e",null);t.default=component.exports},728:function(e,t,n){"use strict";n(699)},729:function(e,t,n){var o=n(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.re-annotation-button[data-v-b966c16e]{width:auto;margin:16px 8px 16px 0;display:inline-flex;position:relative}.re-annotation-button .annotation-button-container[data-v-b966c16e]{display:none}.re-annotation-button.label-button[data-v-b966c16e]{margin:3.5px;color:#353664;padding:0;transition:all .3s ease;max-width:238px}.re-annotation-button.label-button .button[data-v-b966c16e]{outline:none;cursor:pointer;background:#f0f0fe;border-radius:8px;height:40px;line-height:40px;padding-left:.5em;padding-right:.5em;width:100%;display:flex;font-family:"Outfit","Helvetica","Arial",sans-serif;font-weight:500;overflow:hidden;color:#353664;box-shadow:0;transition:all .2s ease-in-out}.re-annotation-button.label-button.predicted-label .button[data-v-b966c16e]{background:#d6d6ff}.re-annotation-button.label-button.active[data-v-b966c16e]{transition:all .2s ease-in-out;box-shadow:none}.re-annotation-button.label-button.active .button[data-v-b966c16e]{transition:all .2s ease-in-out;background:#4c4ea3;box-shadow:none}.re-annotation-button.label-button.active:hover .button[data-v-b966c16e]{transition:all .2s ease-in-out;box-shadow:0 0 1px 0 hsla(0,0%,83.1%,.5),inset 0 -2px 6px 0 #3b3c81}.re-annotation-button.label-button.active[data-v-b966c16e]:after{display:none!important}.re-annotation-button.label-button.active .annotation-button-data__info[data-v-b966c16e],.re-annotation-button.label-button.active .annotation-button-data__score[data-v-b966c16e],.re-annotation-button.label-button.active .annotation-button-data__text[data-v-b966c16e]{color:#fff}.re-annotation-button.label-button .annotation-button-data[data-v-b966c16e]{overflow:hidden;transition:transform .3s ease}.re-annotation-button.label-button .annotation-button-data__text[data-v-b966c16e]{max-width:200px;overflow:hidden;text-overflow:ellipsis;display:inline-block;white-space:nowrap;vertical-align:top}.re-annotation-button.label-button .annotation-button-data__info[data-v-b966c16e]{margin-right:0;margin-left:1em;transform:translateY(0);transition:all .3s ease}.re-annotation-button.label-button .annotation-button-data__score[data-v-b966c16e]{min-width:40px;font-size:12px;font-size:.75rem;display:inline-block;text-align:center;line-height:1.5em;border-radius:2px}.re-annotation-button.label-button:not(.active):hover .button[data-v-b966c16e]{box-shadow:0 0 1px 0 hsla(0,0%,83.1%,.5),inset 0 -2px 6px 1px #bbbce0}.re-annotation-button.disabled[data-v-b966c16e]{opacity:.5}.re-annotation-button.non-reactive[data-v-b966c16e]{pointer-events:none;cursor:pointer}.re-annotation-button.non-reactive .button[data-v-b966c16e]{background:#fff!important;color:#fff;border:1px solid #f2f3f7}.re-annotation-button[data-v-b966c16e]:not(.disabled),.re-annotation-button:not(.disabled) .annotation-button[data-v-b966c16e]{cursor:pointer}.re-annotation-button .annotation-button[data-v-b966c16e]{height:20px;padding-left:8px;line-height:20px}',""]),e.exports=o}}]);