(window.webpackJsonp=window.webpackJsonp||[]).push([[41,17,40],{691:function(e,n,t){var content=t(712);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(93).default)("0e847d56",content,!0,{sourceMap:!1})},711:function(e,n,t){"use strict";t(691)},712:function(e,n,t){var o=t(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.tooltip[data-v-2972dd8e]{position:absolute;background:#4a4a4a;display:inline-block;border-radius:3px;color:#fff;font-size:12px;font-size:.75rem;box-shadow:0 1px 4px 1px hsla(0,0%,87.1%,.5);padding:.1em .5em;white-space:nowrap;left:0;top:calc(100% + 10px)}.tooltip__container[data-v-2972dd8e]{position:relative}.tooltip__container.active[data-v-2972dd8e]  svg{fill:#0508d9!important}.breadcrumbs .tooltip__container.active[data-v-2972dd8e]  svg,.code .tooltip__container.active[data-v-2972dd8e]  svg{fill:#f2067a!important}',""]),e.exports=o},715:function(e,n,t){"use strict";t.r(n);t(82);var o={data:function(){return{showTooltip:!1}},props:{tooltip:{type:String}},methods:{active:function(){var e=this;this.showTooltip=!0,setTimeout((function(){e.showTooltip=void 0}),1e3)}}},r=(t(711),t(50)),component=Object(r.a)(o,(function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("span",{class:["tooltip__container",e.showTooltip?"active":null],on:{click:function(n){return e.active()}}},[e._t("default"),e._v(" "),e.showTooltip&&e.tooltip?t("span",{staticClass:"tooltip"},[e._v(e._s(e.tooltip))]):e._e()],2)}),[],!1,null,"2972dd8e",null);n.default=component.exports},825:function(e,n,t){var content=t(892);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(93).default)("39c1ae59",content,!0,{sourceMap:!1})},891:function(e,n,t){"use strict";t(825)},892:function(e,n,t){var o=t(92)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"Futura Medium";font-style:normal;font-weight:400;font-display:auto;src:local("Futura"),url(/fonts/futura-medium.woff2) format("woff2")}@font-face{font-family:"Futura Medium Condensed";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Medium Condensed"),url(/fonts/futura-medium-condensed.woff2) format("woff2")}@font-face{font-family:"Futura Bold";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Bold"),url(/fonts/futura-bold.woff2) format("woff2")}@font-face{font-family:"Futura Light";font-style:normal;font-weight:400;font-display:auto;src:local("Futura Light"),url(/fonts/futura-light.woff2) format("woff2")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.breadcrumbs[data-v-0766887a]{margin-right:auto;margin-left:1em;display:flex;align-items:center}.breadcrumbs ul[data-v-0766887a]{display:inline-block;padding-left:0;font-weight:400;list-style:none}.breadcrumbs__copy .svg-icon[data-v-0766887a]{fill:#fff}.breadcrumbs__item[data-v-0766887a]{margin:auto .5em auto auto;color:#fff;text-decoration:none;outline:none}.breadcrumbs__item[data-v-0766887a]:not(:last-child):after{content:"/";margin-left:.5em}.breadcrumbs__item[data-v-0766887a]:last-child{font-weight:600}',""]),e.exports=o},996:function(e,n,t){"use strict";t.r(n);t(38),t(14),t(46);var o={props:{breadcrumbs:{type:Array,required:!0},copyButton:{type:Boolean,default:!1}},computed:{filteredBreadcrumbs:function(){return this.breadcrumbs.filter((function(e){return e.name}))}},methods:{copyToClipboard:function(e){var n=document.createElement("input");n.type="text",n.className="hidden-input",n.value=e,document.body.appendChild(n),n.select(),document.execCommand("Copy")}}},r=(t(891),t(50)),component=Object(r.a)(o,(function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"breadcrumbs"},[t("ul",[t("li",e._l(e.filteredBreadcrumbs,(function(n){return t("NuxtLink",{key:n.name,staticClass:"breadcrumbs__item",attrs:{to:n.link}},[e._v("\n        "+e._s(n.name)+"\n      ")])})),1)]),e._v(" "),t("re-action-tooltip",{attrs:{tooltip:"Copied"}},[e.copyButton?t("a",{staticClass:"breadcrumbs__copy",attrs:{href:"#"},on:{click:function(n){return n.preventDefault(),e.copyToClipboard(e.filteredBreadcrumbs[e.filteredBreadcrumbs.length-1].name)}}},[t("svgicon",{attrs:{name:"copy",width:"12",height:"13"}})],1):e._e()])],1)}),[],!1,null,"0766887a",null);n.default=component.exports;installComponents(component,{ReActionTooltip:t(715).default})}}]);