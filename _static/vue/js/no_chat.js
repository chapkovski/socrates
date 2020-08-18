(function(e){function t(t){for(var o,c,i=t[0],r=t[1],u=t[2],l=0,f=[];l<i.length;l++)c=i[l],Object.prototype.hasOwnProperty.call(a,c)&&a[c]&&f.push(a[c][0]),a[c]=0;for(o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o]);d&&d(t);while(f.length)f.shift()();return s.push.apply(s,u||[]),n()}function n(){for(var e,t=0;t<s.length;t++){for(var n=s[t],o=!0,i=1;i<n.length;i++){var r=n[i];0!==a[r]&&(o=!1)}o&&(s.splice(t--,1),e=c(c.s=n[0]))}return e}var o={},a={no_chat:0},s=[];function c(t){if(o[t])return o[t].exports;var n=o[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,c),n.l=!0,n.exports}c.m=e,c.c=o,c.d=function(e,t,n){c.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},c.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},c.t=function(e,t){if(1&t&&(e=c(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(c.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)c.d(n,o,function(t){return e[t]}.bind(null,o));return n},c.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return c.d(t,"a",t),t},c.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},c.p="/static/vue/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],r=i.push.bind(i);i.push=t,i=i.slice();for(var u=0;u<i.length;u++)t(i[u]);var d=r;s.push([2,"chunk-vendors"]),n()})({"0566":function(e,t,n){"use strict";var o=n("dc6f"),a=n.n(o);a.a},2:function(e,t,n){e.exports=n("9ac3")},"595e":function(e,t,n){"use strict";var o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-card",{staticClass:"m-3 content-card d-flex flex-column",attrs:{outlined:!e.enabled,flat:e.enabled}},[n("v-card-text",{staticClass:"content-text d-flex flex-column"},[n("v-card",{staticClass:"mb-3",attrs:{shaped:"",elevation:"24"}},[n("v-card-text",{staticClass:"m-3"},[n("div",{staticClass:"vignette-body light",domProps:{innerHTML:e._s(e.vignette&&e.vignette.body)}})])],1),n("div",{staticClass:"question-wrapper mt-3"},[n("h5",[e._v(e._s(e.vignette.question))]),n("input",{attrs:{type:"hidden",name:"answer"},domProps:{value:e.convertedAnswer}}),n("v-radio-group",{attrs:{mandatory:!1},model:{value:e.answer,callback:function(t){e.answer=t},expression:"answer"}},e._l(e.vignette.choices,(function(t,o){return n("v-radio",{key:o,attrs:{disabled:!e.enabled,label:t.text,value:t.value}})})),1),n("v-card",{attrs:{flat:""}},[n("v-card-text",[n("v-row",{attrs:{align:"center",justify:"center"}},[n("v-col",{attrs:{cols:"12"}},[n("h5",{staticClass:"text-center"},[e._v(" How confident you are in your answer at the scale from "+e._s(e.minConf)+" to "+e._s(e.maxConf)+" ")]),n("input",{attrs:{type:"hidden",name:"confidence"},domProps:{value:e.confidence}})]),n("v-btn-toggle",{model:{value:e.confidence,callback:function(t){e.confidence=t},expression:"confidence"}},e._l(e.confidenceLevels,(function(t,o){return n("v-btn",{key:o,attrs:{disabled:!e.enabled,value:t}},[e._v(" "+e._s(t)+" ")])})),1)],1)],1)],1)],1)],1)],1)},a=[],s=n("2909"),c=n("2ef0"),i=n.n(c),r={props:{vignette:{type:Object,default:function(){}},enabled:{type:Boolean,default:!1}},data:function(){return{confidenceLevels:i.a.range(11),confidence:null,answer:null}},computed:{minConf:function(){return Math.min.apply(Math,Object(s["a"])(this.confidenceLevels))},maxConf:function(){return Math.max.apply(Math,Object(s["a"])(this.confidenceLevels))},convertedAnswer:function(){var e={true:"True",false:"False"};return e[this.answer]}},watch:{confidence:function(e,t){this.$emit("confidence-changed",e)},answer:function(e,t){this.$emit("answer-changed",e)}},mounted:function(){},methods:{}},u=r,d=(n("0566"),n("2877")),l=n("6544"),f=n.n(l),v=n("8336"),g=n("a609"),p=n("b0af"),m=n("99d9"),b=n("62ad"),h=n("67b6"),w=n("43a6"),C=n("0fd9"),O=Object(d["a"])(u,o,a,!1,null,"2c5163f2",null);t["a"]=O.exports;f()(O,{VBtn:v["a"],VBtnToggle:g["a"],VCard:p["a"],VCardText:m["b"],VCol:b["a"],VRadio:h["a"],VRadioGroup:w["a"],VRow:C["a"]})},"9ac3":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var o=n("a026"),a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",{attrs:{id:"inspire"}},[n("v-main",[n("v-container",{staticClass:" main-container",attrs:{fluid:""}},[n("v-row",{staticClass:"limitoverflow",attrs:{align:"center",justify:"center","no-gutters":""}},[n("v-col",{staticClass:"content-col fill-height d-flex flex-column",attrs:{sm:"12"}},[n("v-card",{staticClass:"m-3 content-card d-flex flex-grow-1 flex-column",attrs:{outlined:""}},[n("v-card-text",{staticClass:"d-flex flex-grow-1 flex-column"},[e.vignette?n("formatted-vignette",{attrs:{vignette:e.vignette,enabled:!0},on:{"answer-changed":e.answerChanged,"confidence-changed":e.confidenceChanged}}):e._e()],1),n("v-card-actions",[n("v-btn",{on:{click:e.validateAndSubmit}},[e._v("Next")])],1)],1)],1)],1)],1)],1)],1)},s=[],c=(n("b0c0"),n("5530")),i=n("2f62"),r=n("595e"),u={name:"VignetteNoChat",components:{FormattedVignette:r["a"]},data:function(){return{vignette:null}},mounted:function(){var e=this,t=window.path_to_vignette;this.$http.get(t).then((function(t){e.vignette=t.data,console.debug("VIGNETTE",e.vignette)}))},computed:{currentRouteName:function(){return this.$route.name}},methods:Object(c["a"])(Object(c["a"])({answerChanged:function(e){console.debug("ANSWER CHANGED!!!",e),this.sendDecision({decision_type:"answer",value:e})},confidenceChanged:function(e){console.debug("CONFIENDCE CHANGED!!!",e),this.sendDecision({decision_type:"confidence",value:e})}},Object(i["b"])(["sendMessage"])),{},{validateAndSubmit:function(){console.debug("new form"),document.getElementById("form").submit()}})},d=u,l=n("2877"),f=n("6544"),v=n.n(f),g=n("7496"),p=n("8336"),m=n("b0af"),b=n("99d9"),h=n("62ad"),w=n("a523"),C=n("f6c4"),O=n("0fd9"),_=Object(l["a"])(d,a,s,!1,null,null,null),y=_.exports;v()(_,{VApp:g["a"],VBtn:p["a"],VCard:m["a"],VCardActions:b["a"],VCardText:b["b"],VCol:h["a"],VContainer:w["a"],VMain:C["a"],VRow:O["a"]});n("d1e78"),n("5363");var x=n("ce5b"),E=n.n(x),N=n("2b27"),S=n.n(N),j=(n("bf40"),n("c0d6")),T=n("bc3a"),V=n.n(T);o["default"].prototype.$http=V.a,o["default"].use(E.a),o["default"].use(i["a"]),o["default"].use(S.a),o["default"].config.productionTip=!1,new o["default"]({store:j["a"],vuetify:new E.a({defaultAssets:{font:!0,icons:"mdi"},icons:{iconfont:"mdi"}}),render:function(e){return e(y)}}).$mount("#app")},c0d6:function(e,t,n){"use strict";n("4160"),n("159b");var o=n("a026"),a=n("2f62"),s=n("b408"),c=n.n(s);o["default"].use(a["a"]);var i=new a["a"].Store({state:{id_in_group:window.id_in_group,messages:[],socket:{isConnected:!1,message:"",reconnectError:!1},chatOver:!1,saving:!1},getters:{status:function(e){return console.debug("jopa",e.socket.isConnected),e.socket.isConnected},isChatOver:function(e){return e.chatOver},savingStatus:function(e){return e.saving}},mutations:{SAVING_INITIATED:function(e){e.saving=!0},SAVING_DONE:function(e){e.saving=!1},addMessage:function(e,t){var n=t.owner,o=e.messages[e.messages.length-1];if(o){var a=o.subgroup,s=o.owner;n===s?(t.subgroup=a,o.last=!1,t.last=!0):(t.subgroup=a+1,o.last=!0,t.first=!0,t.last=!0)}else t.subgroup=0,t.first=!0,t.last=!0;e.messages.push(t)},SOCKET_ONOPEN:function(e,t){o["default"].prototype.$socket=t.currentTarget,e.socket.isConnected=!0},SOCKET_ONCLOSE:function(e,t){e.socket.isConnected=!1},SOCKET_ONERROR:function(e,t){console.error(e,t)},SOCKET_ONMESSAGE:function(e,t){},SOCKET_RECONNECT:function(e,t){console.info(e,t)},SOCKET_RECONNECT_ERROR:function(e){e.socket.reconnectError=!0}},actions:{sendMessage:function(e,t){e.commit("addMessage",t),o["default"].prototype.$socket.sendObj(t)},incomingMessage:function(e,t){console.debug("INCOMING messagei incoming",t),e.commit("addMessage",t)},confirm:function(e,t){console.debug("messagei confirmed",t)},requestOldMessages:function(e){var t={request_old_messages:!0};o["default"].prototype.$socket.sendObj(t)},sendDecision:function(e,t){var n={decision:t};o["default"].prototype.$socket.sendObj(n)},PrevMessages:function(e,t){console.debug("previous messages received");var n=t.msgs;n&&n.forEach((function(t){console.debug(t),e.commit("addMessage",t)}))},savingRequested:function(e){var t=e.commit;console.debug("saving request initiated"),t("SAVING_INITIATED")},savingStopRequested:function(e){var t=e.commit;console.debug("saving STOP request initiated"),t("SAVING_DONE")}}}),r="https:"===window.location.protocol?"wss":"ws",u=r+"://"+window.location.host+window.socket_path;o["default"].use(c.a,u,{store:i,format:"json",reconnection:!0,reconnectionAttempts:5,reconnectionDelay:3e3}),t["a"]=i},dc6f:function(e,t,n){}});