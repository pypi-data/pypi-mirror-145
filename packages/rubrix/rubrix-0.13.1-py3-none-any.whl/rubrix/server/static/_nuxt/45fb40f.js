(window.webpackJsonp=window.webpackJsonp||[]).push([[8,37,43,60,90],{1007:function(e,t,n){"use strict";n.r(t);var o=n(18),r=(n(51),n(46),n(182),n(40),n(45),n(39),n(38),n(14),n(56),n(29),n(57),n(44)),c=(n(916),n(181));function d(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,n)}return t}function l(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?d(Object(source),!0).forEach((function(t){Object(o.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):d(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var h={mixins:[Object(c.a)({idProp:function(e){return"".concat(e.dataset.name,"-").concat(e.record.id)}})],props:{allowChangeStatus:{type:Boolean,default:!1},record:{type:r.a,required:!0},dataset:{type:Object},task:{type:String,required:!0}},idState:function(){return{open:!1}},data:function(){return{statusActions:[{name:"Discard",key:"Discarded",class:"discard"}]}},computed:{open:{get:function(){return this.idState.open},set:function(e){this.idState.open=e}},hasMetadata:function(){var e=this.record.metadata;return e&&Object.values(e).length},recordStatus:function(){return this.record.status},allowedStatusActions:function(){var e=this;return this.statusActions.map((function(t){return l(l({},t),{},{isActive:e.recordStatus===t.key})}))}},methods:{onChangeRecordStatus:function(e){this.record.status!==e&&this.$emit("onChangeRecordStatus",e,this.record),this.close()},showMetadata:function(){this.$emit("onShowMetadata"),this.close()},close:function(){this.open=!1}}},f=(n(917),n(50)),component=Object(f.a)(h,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{directives:[{name:"click-outside",rawName:"v-click-outside",value:e.close,expression:"close"}],key:e.open,staticClass:"record__extra-actions"},[e.hasMetadata||e.allowChangeStatus?n("a",{staticClass:"extra-actions__button",attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.open=!e.open}}},[n("svgicon",{attrs:{name:"kebab-menu-v",width:"20",height:"20",color:"#4A4A4A"}})],1):e._e(),e._v(" "),e.open?n("div",{staticClass:"extra-actions__content"},[e.hasMetadata?n("div",{on:{click:function(t){return e.showMetadata()}}},[n("span",[e._v("View metadata")])]):e._e(),e._v(" "),e.allowChangeStatus?e._l(e.allowedStatusActions,(function(t){return n("div",{key:t.key,class:"Discarded"===e.record.status?"disabled":null,on:{click:function(n){return e.onChangeRecordStatus(t.key)}}},[n("span",[e._v(e._s("Discarded"===e.record.status?"Discarded":t.name))])])})):e._e()],2):e._e()])}),[],!1,null,"c241d6de",null);t.default=component.exports},1008:function(e,t,n){"use strict";n.r(t);n(747),n(919),n(920);var o={props:{title:{type:String}}},r=(n(921),n(50)),component=Object(r.a)(o,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("span",{class:["status-tag",e.title]},[n("svgicon",{attrs:{name:"Validated"===e.title?"check":"Edited"===e.title?"clock":"Discarded"===e.title?"forbidden":null,width:"12",height:"12",color:"#ffffff"}}),e._v("\n  "+e._s("Edited"===e.title?"Pending":e.title)+"\n")],1)}),[],!1,null,"23790cd3",null);t.default=component.exports},1052:function(e,t,n){"use strict";n(973)},1053:function(e,t,n){var o=n(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.list__checkbox.re-checkbox[data-v-0f5c1603]{position:absolute;left:1.4em;top:.2em;width:auto}.list__item[data-v-0f5c1603],.list__item--annotation-mode[data-v-0f5c1603]{position:relative;background:#fff;border-radius:1px;display:inline-block;width:100%;transition:.3s ease-in-out;border:1px solid #e9eaed}.list__item--annotation-mode[data-v-0f5c1603]:hover  .edit,.list__item[data-v-0f5c1603]:hover  .edit{opacity:1;pointer-events:all}.list__item__asterisk[data-v-0f5c1603]{font-size:24px;font-size:1.5rem;color:#4c4ea3}.list__item--annotation-mode.discarded[data-v-0f5c1603]{opacity:.5;transition:.3s ease-in-out}.list__item--annotation-mode.discarded[data-v-0f5c1603]:hover{opacity:1;transition:.3s ease-in-out}.list__item__checkbox.re-checkbox[data-v-0f5c1603]{position:absolute;left:1.2em;top:1.2em;width:auto}.list-enter-active[data-v-0f5c1603],.list-leave-active[data-v-0f5c1603]{transition:all .5s ease}.list-enter-from[data-v-0f5c1603],.list-leave-to[data-v-0f5c1603]{opacity:0;transform:translateY(-30px)}',""]),e.exports=o},690:function(e,t,n){var content=n(704);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(93).default)("3afa6990",content,!0,{sourceMap:!1})},696:function(e,t,n){"use strict";n.r(t);n(81),n(95),n(66),n(404),n(702);var o={model:{prop:"areChecked",event:"change"},props:["areChecked","value","id","disabled"],data:function(){return{checked:this.value||!1}},computed:{classes:function(){return{checked:Array.isArray(this.areChecked)?this.areChecked.includes(this.value):this.checked,disabled:this.disabled}}},watch:{value:function(){this.checked=!!this.value},areChecked:function(e){"boolean"==typeof e&&(this.checked=e)}},methods:{toggleCheck:function(){if(!this.disabled)if(Array.isArray(this.areChecked)){var e=this.areChecked.slice(),t=e.indexOf(this.value);-1!==t?e.splice(t,1):e.push(this.value),this.$emit("change",e)}else{this.checked=!this.checked;var n=this.areChecked;n=this.checked,this.$emit("change",n),this.$emit("input",n)}}}},r=(n(703),n(50)),component=Object(r.a)(o,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"re-checkbox",class:[e.classes]},[e.$slots.default?n("label",{staticClass:"checkbox-label",attrs:{for:e.id},on:{click:function(t){return t.preventDefault(),e.toggleCheck.apply(null,arguments)}}},[e._t("default")],2):e._e(),e._v(" "),n("div",{staticClass:"checkbox-container",attrs:{tabindex:"0"},on:{click:function(t){return t.stopPropagation(),e.toggleCheck.apply(null,arguments)}}},[n("input",{attrs:{id:e.id,type:"checkbox",disabled:e.disabled},domProps:{value:e.value,checked:e.checked}}),e._v(" "),n("svgicon",{attrs:{color:"#fffff",width:"12",name:"check2"}})],1)])}),[],!1,null,"51221cf6",null);t.default=component.exports},702:function(e,t,n){n(176).register({check2:{width:12,height:9,viewBox:"0 0 12 9",data:'<path pid="0" d="M10.633 0c-.345.01-.673.142-.914.37-2.073 1.913-3.671 3.516-5.57 5.307L2.217 4.173a1.416 1.416 0 00-1.326-.246c-.457.147-.792.51-.873.95-.081.44.103.885.482 1.163l2.88 2.242c.527.411 1.31.38 1.799-.07 2.39-2.204 4.087-3.962 6.422-6.116.39-.352.506-.889.292-1.352-.214-.463-.715-.758-1.261-.743z" _fill="#FFF" fill-rule="nonzero"/>'}})},703:function(e,t,n){"use strict";n(690)},704:function(e,t,n){var o=n(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.re-checkbox[data-v-51221cf6]{width:auto;margin:16px 8px 16px 0;display:inline-flex;position:relative;border-radius:1px}.re-checkbox.disabled[data-v-51221cf6]{opacity:.6}.re-checkbox[data-v-51221cf6]:not(.disabled),.re-checkbox:not(.disabled) .checkbox-label[data-v-51221cf6]{cursor:pointer}.re-checkbox .checkbox-container[data-v-51221cf6]{width:20px;min-width:20px;height:20px;position:relative;border-radius:1px;border:1px solid #e9eaed;vertical-align:middle;text-align:center}.re-checkbox .checkbox-container .svg-icon[data-v-51221cf6]{fill:#fff;transform:scale(0);transition:all .2s ease-in-out;display:block;margin:2px auto auto}.re-checkbox .checkbox-container[data-v-51221cf6]:focus{outline:none}.re-checkbox .checkbox-container input[data-v-51221cf6]{position:absolute;left:-999em}.re-checkbox .checkbox-label[data-v-51221cf6]{height:20px;line-height:20px;margin-right:auto}.re-checkbox--dark.checked .checkbox-label[data-v-51221cf6]{color:#0508d9}.re-checkbox--dark .checkbox-container[data-v-51221cf6]{border:1px solid #0508d9}.re-checkbox--dark .checkbox-container[data-v-51221cf6]:after{background:#0508d9}.dropdown--filter .checkbox-label[data-v-51221cf6]{height:auto;padding-right:2em;white-space:normal;text-transform:none}.re-checkbox.checked .checkbox-container[data-v-51221cf6]{background:#0508d9;border:1px solid #0508d9}.re-checkbox.checked .checkbox-container .svg-icon[data-v-51221cf6]{transform:scale(1);transition:all .2s ease-in-out}',""]),e.exports=o},747:function(e,t,n){n(176).register({check:{width:10,height:8,viewBox:"0 0 10 8",data:'<path pid="0" d="M2.102 3.767A.9.9 0 10.786 4.995L2.92 7.281a.9.9 0 001.316 0l4.978-5.334A.9.9 0 107.898.72l-4.32 4.629-1.476-1.581z" _fill="#FFF" fill-rule="nonzero"/>'}})},842:function(e,t,n){var content=n(918);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(93).default)("e86fd960",content,!0,{sourceMap:!1})},843:function(e,t,n){var content=n(922);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(93).default)("53181b3a",content,!0,{sourceMap:!1})},879:function(e,t,n){"use strict";n.r(t);n(45),n(39),n(38),n(56),n(29),n(57);var o=n(1),r=n(18),c=(n(33),n(177),n(14),n(94));function d(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,n)}return t}function l(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?d(Object(source),!0).forEach((function(t){Object(r.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):d(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var h={props:{dataset:{type:Object,required:!0},item:{type:Object,required:!0}},computed:{annotationEnabled:function(){return"annotate"===this.dataset.viewSettings.viewMode},visibleRecords:function(){return this.dataset.visibleRecords}},methods:l(l({},Object(c.b)({updateRecords:"entities/datasets/updateDatasetRecords",discard:"entities/datasets/discardAnnotations",validate:"entities/datasets/validateAnnotations"})),{},{onCheckboxChanged:function(e,t){var n=this;return Object(o.a)(regeneratorRuntime.mark((function o(){var r;return regeneratorRuntime.wrap((function(o){for(;;)switch(o.prev=o.next){case 0:return r=n.visibleRecords.find((function(e){return e.id===t})),o.next=3,n.updateRecords({dataset:n.dataset,records:[l(l({},r),{},{selected:e})]});case 3:case"end":return o.stop()}}),o)})))()},onChangeRecordStatus:function(e,t){var n=this;return Object(o.a)(regeneratorRuntime.mark((function o(){return regeneratorRuntime.wrap((function(o){for(;;)switch(o.prev=o.next){case 0:o.t0=e,o.next="Validated"===o.t0?3:"Discarded"===o.t0?6:9;break;case 3:return o.next=5,n.validate({dataset:n.dataset,records:[t]});case 5:return o.abrupt("break",10);case 6:return o.next=8,n.discard({dataset:n.dataset,records:[t]});case 8:return o.abrupt("break",10);case 9:console.warn("waT?",e);case 10:case"end":return o.stop()}}),o)})))()},onShowMetadata:function(e){this.$emit("show-metadata",e)}})},f=(n(1052),n(50)),component=Object(f.a)(h,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{class:[e.annotationEnabled?"list__item--annotation-mode":"list__item","Discarded"===e.item.status?"discarded":null]},[e.annotationEnabled?n("ReCheckbox",{staticClass:"list__checkbox",attrs:{value:e.item.selected},on:{change:function(t){return e.onCheckboxChanged(t,e.item.id)}}}):e._e(),e._v(" "),e._t("default",null,{record:e.item}),e._v(" "),n("RecordExtraActions",{key:e.item.id,attrs:{"allow-change-status":e.annotationEnabled,record:e.item,dataset:e.dataset,task:e.dataset.task},on:{onChangeRecordStatus:e.onChangeRecordStatus,onShowMetadata:function(t){return e.onShowMetadata(e.item)}}}),e._v(" "),e.annotationEnabled&&"Default"!==e.item.status?n("status-tag",{attrs:{title:e.item.status}}):e._e()],2)])}),[],!1,null,"0f5c1603",null);t.default=component.exports;installComponents(component,{ReCheckbox:n(696).default,RecordExtraActions:n(1007).default,StatusTag:n(1008).default})},916:function(e,t,n){n(176).register({"kebab-menu-v":{width:3,height:12,viewBox:"0 0 3 12",data:'<path pid="0" d="M1.49.837c.382 0 .671.103.867.308.196.205.294.504.294.896 0 .378-.1.67-.3.878-.201.207-.488.311-.862.311-.36 0-.644-.105-.85-.314-.208-.21-.312-.502-.312-.875 0-.383.102-.68.304-.89.203-.209.49-.314.858-.314zm0 3.986c.382 0 .671.102.867.307.196.205.294.506.294.903 0 .378-.1.67-.3.878-.201.207-.488.311-.862.311-.36 0-.644-.105-.85-.314-.208-.21-.312-.502-.312-.875 0-.388.102-.686.304-.896.203-.21.49-.314.858-.314zm0 3.992c.382 0 .671.102.867.308.196.205.294.503.294.895 0 .378-.1.671-.3.878-.201.208-.488.312-.862.312-.36 0-.644-.105-.85-.315-.208-.21-.312-.501-.312-.875 0-.383.102-.679.304-.889.203-.21.49-.314.858-.314z" _fill="red" fill-rule="evenodd"/>'}})},917:function(e,t,n){"use strict";n(842)},918:function(e,t,n){var o=n(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.record__extra-actions[data-v-c241d6de]{position:absolute;top:1.5em;right:.9em}.extra-actions[data-v-c241d6de]{position:relative}.extra-actions__button[data-v-c241d6de]{text-align:right;outline:none;text-decoration:none}.extra-actions__content[data-v-c241d6de]{position:absolute;right:.7em;top:2em;background:#fff;border-radius:5px;box-shadow:0 8px 20px 0 rgba(93,105,151,.3);padding:3px;min-width:135px;z-index:1}.extra-actions__content .disabled[data-v-c241d6de]{pointer-events:none}.extra-actions__content div[data-v-c241d6de]{padding:.5em;color:#353664;cursor:pointer;display:block;background:#fff;transition:background .3s ease-in-out}.extra-actions__content div[data-v-c241d6de]:first-child{border-top-left-radius:5px;border-top-right-radius:5px}.extra-actions__content div[data-v-c241d6de]:last-child{border-bottom-left-radius:5px;border-bottom-right-radius:5px}.extra-actions__content div[data-v-c241d6de]:hover{transition:background .3s ease-in-out;background:#f5f5f5}',""]),e.exports=o},919:function(e,t,n){n(176).register({clock:{width:13,height:13,viewBox:"0 0 13 13",data:'<g _fill="#FFF" fill-rule="nonzero"><path pid="0" d="M10.128.217H2.872C1.313.217.092 1.84.092 3.914v5.172c0 2.074 1.221 3.697 2.78 3.697h7.256c1.56 0 2.78-1.624 2.78-3.697V3.914c0-2.073-1.22-3.697-2.78-3.697zm1.047 8.87c0 1.105-.563 1.963-1.047 1.963H2.872c-.484 0-1.047-.858-1.047-1.964V3.914c0-1.106.563-1.964 1.047-1.964h7.256c.484 0 1.047.858 1.047 1.964v5.172z"/><path pid="1" d="M7.747 5.676h-.612v-.528a.796.796 0 00-1.592 0V6.47c0 .44.356.796.796.796l.033-.003c.017.001.034.005.052.005h1.323a.796.796 0 000-1.592z"/></g>'}})},920:function(e,t,n){n(176).register({forbidden:{width:13,height:13,viewBox:"0 0 13 13",data:'<path pid="0" d="M6.5 0a6.5 6.5 0 110 13 6.5 6.5 0 010-13zm4.194 3.072l-7.622 7.622a5.417 5.417 0 007.622-7.622zM2.306 9.928l7.622-7.622a5.417 5.417 0 00-7.622 7.622z" _fill="#FFF" fill-rule="nonzero"/>'}})},921:function(e,t,n){"use strict";n(843)},922:function(e,t,n){var o=n(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.status-tag[data-v-23790cd3]{position:absolute;top:1em;right:3.6em;display:flex;align-items:center;background:#4c4ea3;color:#fff;border-radius:50px;padding:.7em 1em;font-size:12px;font-size:.75rem;font-weight:600;z-index:0}.status-tag.Edited[data-v-23790cd3]{background:#bb720a}.status-tag.Discarded[data-v-23790cd3]{background:#70767f}.status-tag .svg-icon[data-v-23790cd3]{margin-right:.5em}',""]),e.exports=o},973:function(e,t,n){var content=n(1053);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(93).default)("151415e1",content,!0,{sourceMap:!1})}}]);