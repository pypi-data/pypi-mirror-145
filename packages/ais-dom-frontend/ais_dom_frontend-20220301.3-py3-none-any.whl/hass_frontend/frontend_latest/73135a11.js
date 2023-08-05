/*! For license information please see 73135a11.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[73245],{63207:(e,t,i)=>{i(65660),i(15112);var r=i(9672),n=i(87156),o=i(50856),a=i(10994);(0,r.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:a.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,n.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,n.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{i.d(t,{P:()=>n});i(10994);var r=i(9672);class n{constructor(e){n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(e){return o[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}n[" "]=function(){},n.types={};var o=n.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var r=new n({type:e,key:t});return void 0!==i&&i!==r.value?r.value=i:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new n({type:this.type,key:e}).value}})},21560:(e,t,i)=>{i.d(t,{ZH:()=>d,MT:()=>o,U2:()=>l,RV:()=>n,t8:()=>c});const r=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let e;return new Promise((t=>{const i=()=>indexedDB.databases().finally(t);e=setInterval(i,100),i()})).finally((()=>clearInterval(e)))};function n(e){return new Promise(((t,i)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>i(e.error)}))}function o(e,t){const i=r().then((()=>{const i=indexedDB.open(e);return i.onupgradeneeded=()=>i.result.createObjectStore(t),n(i)}));return(e,r)=>i.then((i=>r(i.transaction(t,e).objectStore(t))))}let a;function s(){return a||(a=o("keyval-store","keyval")),a}function l(e,t=s()){return t("readonly",(t=>n(t.get(e))))}function c(e,t,i=s()){return i("readwrite",(i=>(i.put(t,e),n(i.transaction))))}function d(e=s()){return e("readwrite",(e=>(e.clear(),n(e.transaction))))}},25516:(e,t,i)=>{i.d(t,{i:()=>r});const r=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){this[`__${String(t.key)}`]=e},get(){return this[`__${String(t.key)}`]},enumerable:!0,configurable:!0},finisher(i){const r=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(r.call(this),this[t.key]){const i=this.renderRoot.querySelector(e);if(!i)return;i.scrollTop=this[t.key]}}}})},27269:(e,t,i)=>{i.d(t,{p:()=>r});const r=e=>e.substr(e.indexOf(".")+1)},22311:(e,t,i)=>{i.d(t,{N:()=>n});var r=i(58831);const n=e=>(0,r.M)(e.entity_id)},91741:(e,t,i)=>{i.d(t,{C:()=>n});var r=i(27269);const n=e=>void 0===e.attributes.friendly_name?(0,r.p)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},85415:(e,t,i)=>{i.d(t,{$:()=>r,f:()=>n});const r=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>r(e.toLowerCase(),t.toLowerCase())},73728:(e,t,i)=>{i.d(t,{pV:()=>a,P3:()=>s,Ky:()=>c,D4:()=>d,XO:()=>p,zO:()=>h,oi:()=>u,d4:()=>f,D7:()=>v,ZJ:()=>m,V3:()=>g,WW:()=>_});var r=i(97330),n=i(38346),o=i(5986);const a=["usb","unignore","dhcp","homekit","ssdp","zeroconf","discovery","integration_discovery","mqtt","hassio"],s=["reauth"],l={"HA-Frontend-Base":`${location.protocol}//${location.host}`},c=(e,t)=>{var i;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(i=e.userData)||void 0===i?void 0:i.showAdvanced)},l)},d=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,l),p=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i,l),h=(e,t,i)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t,title:i}),u=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),f=e=>e.callApi("GET","config/config_entries/flow_handlers"),v=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),y=(e,t)=>e.subscribeEvents((0,n.D)((()=>v(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),m=e=>(0,r._)(e,"_configFlowProgress",v,y),g=(e,t)=>m(e.connection).subscribe(t),_=(e,t)=>t.context.title_placeholders&&0!==Object.keys(t.context.title_placeholders).length?e(`component.${t.handler}.config.flow_title`,t.context.title_placeholders)||("name"in t.context.title_placeholders?t.context.title_placeholders.name:(0,o.Lh)(e,t.handler)):(0,o.Lh)(e,t.handler)},57292:(e,t,i)=>{i.d(t,{jL:()=>s,t1:()=>l,dl:()=>c,_Y:()=>d,q4:()=>h,Wg:()=>u});var r=i(97330),n=i(91741),o=i(85415),a=i(38346);const s=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,r=e.states[t];if(r)return(0,n.C)(r)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device","type",t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)),l=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),c=(e,t,i)=>e.callWS({type:"config/device_registry/remove_config_entry",device_id:t,config_entry_id:i}),d=e=>e.sendMessagePromise({type:"config/device_registry/list"}),p=(e,t)=>e.subscribeEvents((0,a.D)((()=>d(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),h=(e,t)=>(0,r.B)("_dr",d,p,e,t),u=e=>e.sort(((e,t)=>(0,o.f)(e.name||"",t.name||"")))},60633:(e,t,i)=>{i.d(t,{N8:()=>r,E0:()=>n,PH:()=>o,BM:()=>a,HV:()=>s,mB:()=>l,qc:()=>c,fQ:()=>d});const r=0,n=5,o=7,a=10,s=e=>e.callWS({type:"zwave/network_status"}),l=e=>e.callWS({type:"zwave/start_zwave_js_config_flow"}),c=e=>e.callWS({type:"zwave/get_migration_config"}),d=(e,t)=>e.callApi("GET",`zwave/config/${t}`)},62770:(e,t,i)=>{let r,n,o,a;var s,l;i.d(t,{TW:()=>r,tt:()=>n,is:()=>o,Uf:()=>a,N2:()=>c,Fy:()=>p,x1:()=>h,OV:()=>u,aK:()=>f,rs:()=>v,pr:()=>y,wz:()=>m,PE:()=>g,tY:()=>_,xK:()=>w,Qf:()=>k,JT:()=>b,BP:()=>S,f$:()=>E,vS:()=>z,mZ:()=>D,Mb:()=>$,kL:()=>C,yD:()=>x,vN:()=>P,uq:()=>A,Hr:()=>j,OF:()=>W,Ir:()=>T,M0:()=>I,EW:()=>O,T5:()=>N,LD:()=>Z,Db:()=>F,xw:()=>B}),function(e){e[e.Idle=0]="Idle",e[e.Including=1]="Including",e[e.Excluding=2]="Excluding",e[e.Busy=3]="Busy",e[e.SmartStart=4]="SmartStart"}(r||(r={})),function(e){e[e.Default=0]="Default",e[e.SmartStart=1]="SmartStart",e[e.Insecure=2]="Insecure",e[e.Security_S0=3]="Security_S0",e[e.Security_S2=4]="Security_S2"}(n||(n={})),function(e){e[e.Temporary=-2]="Temporary",e[e.None=-1]="None",e[e.S2_Unauthenticated=0]="S2_Unauthenticated",e[e.S2_Authenticated=1]="S2_Authenticated",e[e.S2_AccessControl=2]="S2_AccessControl",e[e.S0_Legacy=7]="S0_Legacy"}(o||(o={})),function(e){e[e.SmartStart=0]="SmartStart"}(a||(a={})),function(e){e[e.S2=0]="S2",e[e.SmartStart=1]="SmartStart"}(s||(s={})),function(e){e[e.ZWave=0]="ZWave",e[e.ZWaveLongRange=1]="ZWaveLongRange"}(l||(l={}));const c=52;let d;!function(e){e[e.Unknown=0]="Unknown",e[e.Asleep=1]="Asleep",e[e.Awake=2]="Awake",e[e.Dead=3]="Dead",e[e.Alive=4]="Alive"}(d||(d={}));const p=32143==i.j?["unknown","asleep","awake","dead","alive"]:null,h=(e,t,i=!0)=>e.callWS({type:"zwave_js/migrate_zwave",entry_id:t,dry_run:i}),u=(e,t)=>e.callWS({type:"zwave_js/network_status",entry_id:t}),f=(e,t)=>e.callWS({type:"zwave_js/data_collection_status",entry_id:t}),v=(e,t,i)=>e.callWS({type:"zwave_js/update_data_collection_preference",entry_id:t,opted_in:i}),y=(e,t)=>e.callWS({type:"zwave_js/get_provisioning_entries",entry_id:t}),m=(e,t,i,r=n.Default,o,a,s)=>e.connection.subscribeMessage((e=>i(e)),{type:"zwave_js/add_node",entry_id:t,inclusion_strategy:r,qr_code_string:a,qr_provisioning_information:o,planned_provisioning_entry:s}),g=(e,t)=>e.callWS({type:"zwave_js/stop_inclusion",entry_id:t}),_=(e,t)=>e.callWS({type:"zwave_js/stop_exclusion",entry_id:t}),w=(e,t,i,r)=>e.callWS({type:"zwave_js/grant_security_classes",entry_id:t,security_classes:i,client_side_auth:r}),k=(e,t,i)=>e.callWS({type:"zwave_js/validate_dsk_and_enter_pin",entry_id:t,pin:i}),b=(e,t,i)=>e.callWS({type:"zwave_js/supports_feature",entry_id:t,feature:i}),S=(e,t,i)=>e.callWS({type:"zwave_js/parse_qr_code_string",entry_id:t,qr_code_string:i}),E=(e,t,i,r,n)=>e.callWS({type:"zwave_js/provision_smart_start_node",entry_id:t,qr_code_string:r,qr_provisioning_information:i,planned_provisioning_entry:n}),z=(e,t,i,r)=>e.callWS({type:"zwave_js/unprovision_smart_start_node",entry_id:t,dsk:i,node_id:r}),D=(e,t,i)=>e.callWS({type:"zwave_js/node_status",entry_id:t,node_id:i}),$=(e,t,i)=>e.callWS({type:"zwave_js/node_metadata",entry_id:t,node_id:i}),C=(e,t,i)=>e.callWS({type:"zwave_js/get_config_parameters",entry_id:t,node_id:i}),x=(e,t,i,r,n,o)=>{const a={type:"zwave_js/set_config_parameter",entry_id:t,node_id:i,property:r,value:n,property_key:o};return e.callWS(a)},P=(e,t,i,r)=>e.connection.subscribeMessage((e=>r(e)),{type:"zwave_js/refresh_node_info",entry_id:t,node_id:i}),A=(e,t,i)=>e.callWS({type:"zwave_js/heal_node",entry_id:t,node_id:i}),j=(e,t,i,r)=>e.connection.subscribeMessage((e=>r(e)),{type:"zwave_js/remove_failed_node",entry_id:t,node_id:i}),W=(e,t)=>e.callWS({type:"zwave_js/begin_healing_network",entry_id:t}),T=(e,t)=>e.callWS({type:"zwave_js/stop_healing_network",entry_id:t}),I=(e,t,i,r)=>e.connection.subscribeMessage((e=>r(e)),{type:"zwave_js/node_ready",entry_id:t,node_id:i}),O=(e,t,i)=>e.connection.subscribeMessage((e=>i(e)),{type:"zwave_js/subscribe_heal_network_progress",entry_id:t}),N=e=>{if(!e)return;const t=e.identifiers.find((e=>"zwave_js"===e[0]));if(!t)return;const i=t[1].split("-");return{node_id:parseInt(i[1]),home_id:i[0]}},Z=(e,t,i)=>e.connection.subscribeMessage(i,{type:"zwave_js/subscribe_log_updates",entry_id:t}),F=(e,t)=>e.callWS({type:"zwave_js/get_log_config",entry_id:t}),B=(e,t,i)=>e.callWS({type:"zwave_js/update_log_config",entry_id:t,config:{level:i}})},2852:(e,t,i)=>{i.d(t,{t:()=>l});var r=i(37500),n=i(85415),o=i(73728),a=i(5986),s=i(52871);const l=(e,t)=>(0,s.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,o.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,i)=>(0,n.f)((0,a.Lh)(e.localize,t),(0,a.Lh)(e.localize,i))))},createFlow:async(e,t)=>{const[i]=await Promise.all([(0,o.Ky)(e,t),e.loadBackendTranslation("config",t),e.loadBackendTranslation("title",t)]);return i},fetchFlow:async(e,t)=>{const i=await(0,o.D4)(e,t);return await e.loadBackendTranslation("config",i.handler),i},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(e,t){const i=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?r.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const i=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?r.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,i)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${i.name}`),renderShowFormStepFieldError:(e,t,i)=>e.localize(`component.${t.handler}.config.error.${i}`,t.description_placeholders),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const i=e.localize(`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return r.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?r.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=e.localize(`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return r.dy`
        ${i?r.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const i=e.localize(`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return i?r.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderLoadingDescription(e,t,i,r){if(!["loading_flow","loading_step"].includes(t))return"";const n=(null==r?void 0:r.handler)||i;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:n?(0,a.Lh)(e.localize,n):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},52871:(e,t,i)=>{i.d(t,{w:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(29563),i.e(98985),i.e(24103),i.e(59799),i.e(6294),i.e(41985),i.e(88278),i.e(85084),i.e(45507),i.e(5906),i.e(68200),i.e(49842),i.e(49075),i.e(1548),i.e(25782),i.e(81480),i.e(7221),i.e(22040),i.e(12545),i.e(13701),i.e(77576),i.e(65040),i.e(68101),i.e(4940),i.e(17643),i.e(52736)]).then(i.bind(i,63118)),o=(e,t,i)=>{(0,r.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...t,flowConfig:i}})}},60010:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(25516);i(2315),i(48932);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function s(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=a();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var p=t((function(e){n.initializeInstanceElements(e,h.elements)}),i),h=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(p.d.map(s)),e);n.initializeClassElements(p.F,h.elements),n.runClassFinishers(p.F,h.finishers)}([(0,n.Mo)("hass-subpage")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[(0,o.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"render",value:function(){var e;return r.dy`
      <div class="toolbar">
        ${this.mainPage||null!==(e=history.state)&&void 0!==e&&e.root?r.dy`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?r.dy`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:r.dy`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}

        <div class="main-title">${this.header}</div>
        <slot name="toolbar-icon"></slot>
      </div>
      <div class="content" @scroll=${this._saveScrollPos}><slot></slot></div>
    `}},{kind:"method",decorators:[(0,n.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        padding: 0 16px;
        pointer-events: none;
        background-color: var(--app-header-background-color);
        font-weight: 400;
        color: var(--app-header-text-color, white);
        border-bottom: var(--app-header-border-bottom, none);
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--sidebar-text-color);
        text-decoration: none;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        pointer-events: auto;
      }

      .main-title {
        margin: 0 0 0 24px;
        line-height: 20px;
        flex-grow: 1;
      }

      .content {
        position: relative;
        width: 100%;
        height: calc(100% - 1px - var(--header-height));
        overflow-y: auto;
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }
    `}}]}}),r.oi)},41896:(e,t,i)=>{i.r(t),i.d(t,{ZwaveMigration:()=>b});i(51187),i(53268),i(12730);var r=i(37500),n=i(33310),o=i(7323),a=i(22311),s=i(91741),l=(i(94132),i(54909),i(9381),i(22098),i(34552),i(28007),i(10983),i(57292)),c=i(60633),d=i(62770),p=i(2852),h=i(26765),u=(i(60010),i(11654));i(88165);function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return k(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?k(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=w(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:_(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=_(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function v(e){var t,i=w(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function w(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function k(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}let b=function(e,t,i,r){var n=f();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(g(o.descriptor)||g(n.descriptor)){if(m(o)||m(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(m(o)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}y(o,n)}else t.push(o)}return t}(a.d.map(v)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("zwave-migration")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_networkStatus",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_step",value:()=>0},{kind:"field",decorators:[(0,n.SB)()],key:"_stoppingNetwork",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_migrationConfig",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_migrationData",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_migratedZwaveEntities",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_deviceNameLookup",value:()=>({})},{kind:"field",decorators:[(0,n.SB)()],key:"_waitingOnDevices",value:void 0},{kind:"field",key:"_zwaveJsEntryId",value:void 0},{kind:"field",key:"_nodeReadySubscriptions",value:void 0},{kind:"field",key:"_unsub",value:void 0},{kind:"field",key:"_unsubDevices",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){this._unsubscribe(),this._unsubDevices&&(this._unsubDevices(),this._unsubDevices=void 0)}},{kind:"method",key:"render",value:function(){var e;return r.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        back-path="/config/zwave"
      >
        <ha-config-section .narrow=${this.narrow} .isWide=${this.isWide}>
          <div slot="header">
            ${this.hass.localize("ui.panel.config.zwave.migration.zwave_js.header")}
          </div>

          <div slot="introduction">
            ${this.hass.localize("ui.panel.config.zwave.migration.zwave_js.introduction")}
          </div>
          ${r.dy`
            ${0===this._step?r.dy`
                  <ha-card class="content" header="Introduction">
                    <div class="card-content">
                      <p>
                        This wizard will walk through the following steps to
                        migrate from the legacy Z-Wave integration to Z-Wave JS.
                      </p>
                      <ol>
                        <li>Stop the Z-Wave network</li>
                        ${(0,o.p)(this.hass,"hassio")?"":r.dy`<li>Configure and start Z-Wave JS</li>`}
                        <li>Set up the Z-Wave JS integration</li>
                        <li>
                          Migrate entities and devices to the new integration
                        </li>
                        <li>Remove legacy Z-Wave integration</li>
                      </ol>
                      <p>
                        <b>
                          ${(0,o.p)(this.hass,"hassio")?r.dy`Please
                                <a href="/hassio/backups">make a backup</a>
                                before proceeding.`:"Please make a backup of your installation before proceeding."}
                        </b>
                      </p>
                    </div>
                    <div class="card-actions">
                      <mwc-button @click=${this._continue}>
                        Continue
                      </mwc-button>
                    </div>
                  </ha-card>
                `:1===this._step?r.dy`
                  <ha-card class="content" header="Stop Z-Wave Network">
                    <div class="card-content">
                      <p>
                        We need to stop the Z-Wave network to perform the
                        migration. Home Assistant will not be able to control
                        Z-Wave devices while the network is stopped.
                      </p>
                      ${Object.values(this.hass.states).filter((e=>"zwave"===(0,a.N)(e)&&!["ready","sleeping"].includes(e.state))).map((e=>r.dy`<ha-alert alert-type="warning">
                              Device ${(0,s.C)(e)}
                              (${e.entity_id}) is not ready yet! For
                              the best result, wake the device up if it is
                              battery powered and wait for this device to become
                              ready.
                            </ha-alert>`))}
                      ${this._stoppingNetwork?r.dy`
                            <div class="flex-container">
                              <ha-circular-progress
                                active
                              ></ha-circular-progress>
                              <div><p>Stopping Z-Wave Network...</p></div>
                            </div>
                          `:""}
                    </div>
                    <div class="card-actions">
                      <mwc-button @click=${this._stopNetwork}>
                        Stop Network
                      </mwc-button>
                    </div>
                  </ha-card>
                `:2===this._step?r.dy`
                  <ha-card class="content" header="Set up Z-Wave JS">
                    <div class="card-content">
                      <p>Now it's time to set up the Z-Wave JS integration.</p>
                      ${(0,o.p)(this.hass,"hassio")?r.dy`
                            <p>
                              Z-Wave JS runs as a Home Assistant add-on that
                              will be setup next. Make sure to check the
                              checkbox to use the add-on.
                            </p>
                          `:r.dy`
                            <p>
                              You are not running Home Assistant OS (the default
                              installation type) or Home Assistant Supervised,
                              so we can not setup Z-Wave JS automaticaly. Follow
                              the
                              <a
                                href="https://www.home-assistant.io/integrations/zwave_js/#advanced-installation-instructions"
                                target="_blank"
                                rel="noreferrer"
                                >advanced installation instructions</a
                              >
                              to install Z-Wave JS.
                            </p>
                            <p>
                              Here's the current Z-Wave configuration. You'll
                              need these values when setting up Z-Wave JS.
                            </p>
                            ${this._migrationConfig?r.dy`<blockquote>
                                  USB Path: ${this._migrationConfig.usb_path}<br />
                                  Network Key:
                                  ${this._migrationConfig.network_key}
                                </blockquote>`:""}
                            <p>
                              Once Z-Wave JS is installed and running, click
                              'Continue' to set up the Z-Wave JS integration and
                              migrate your devices and entities.
                            </p>
                          `}
                    </div>
                    <div class="card-actions">
                      <mwc-button @click=${this._setupZwaveJs}>
                        Continue
                      </mwc-button>
                    </div>
                  </ha-card>
                `:3===this._step?r.dy`
                  <ha-card
                    class="content"
                    header="Migrate devices and entities"
                  >
                    <div class="card-content">
                      <p>
                        Now it's time to migrate your devices and entities from
                        the legacy Z-Wave integration to the Z-Wave JS
                        integration, to make sure all your UI's and automations
                        keep working.
                      </p>
                      ${null===(e=this._waitingOnDevices)||void 0===e?void 0:e.map((e=>r.dy`<ha-alert alert-type="warning">
                            Device ${(0,l.jL)(e,this.hass)} is
                            not ready yet! For the best result, wake the device
                            up if it is battery powered and wait for this device
                            to become ready.
                          </ha-alert>`))}
                      ${this._migrationData?r.dy`
                            <p>Below is a list of what will be migrated.</p>
                            ${this._migratedZwaveEntities.length!==this._migrationData.zwave_entity_ids.length?r.dy`<ha-alert
                                    alert-type="warning"
                                    title="Not all entities can be migrated!"
                                  >
                                    The following entities will not be migrated
                                    and might need manual adjustments to your
                                    config:
                                  </ha-alert>
                                  <ul>
                                    ${this._migrationData.zwave_entity_ids.map((e=>this._migratedZwaveEntities.includes(e)?"":r.dy`<li>
                                              ${e in this.hass.states?(0,s.C)(this.hass.states[e]):""}
                                              (${e})
                                            </li>`))}
                                  </ul>`:""}
                            ${Object.keys(this._migrationData.migration_device_map).length?r.dy`<h3>Devices that will be migrated:</h3>
                                  <ul>
                                    ${Object.keys(this._migrationData.migration_device_map).map((e=>r.dy`<li>
                                          ${this._deviceNameLookup[e]||e}
                                        </li>`))}
                                  </ul>`:""}
                            ${Object.keys(this._migrationData.migration_entity_map).length?r.dy`<h3>Entities that will be migrated:</h3>
                                  <ul>
                                    ${Object.keys(this._migrationData.migration_entity_map).map((e=>r.dy`<li>
                                        ${e in this.hass.states?(0,s.C)(this.hass.states[e]):""}
                                        (${e})
                                      </li>`))}
                                  </ul>`:""}
                          `:r.dy` <div class="flex-container">
                            <p>Loading migration data...</p>
                            <ha-circular-progress active>
                            </ha-circular-progress>
                          </div>`}
                    </div>
                    <div class="card-actions">
                      <mwc-button @click=${this._doMigrate}>
                        Migrate
                      </mwc-button>
                    </div>
                  </ha-card>
                `:4===this._step?r.dy`<ha-card class="content" header="Done!">
                  <div class="card-content">
                    That was all! You are now migrated to the new Z-Wave JS
                    integration, check if all your devices and entities are back
                    the way they where, if not all entities could be migrated
                    you might have to change those manually.
                    <p>
                      If you have 'zwave' in your configurtion.yaml file, you
                      should remove it now.
                    </p>
                  </div>
                  <div class="card-actions">
                    <a
                      href=${`/config/zwave_js?config_entry=${this._zwaveJsEntryId}`}
                    >
                      <mwc-button> Go to Z-Wave JS config panel </mwc-button>
                    </a>
                  </div>
                </ha-card>`:""}
          `}
        </ha-config-section>
      </hass-subpage>
    `}},{kind:"method",key:"_getMigrationConfig",value:async function(){this._migrationConfig=await(0,c.qc)(this.hass)}},{kind:"method",key:"_unsubscribe",value:async function(){this._unsub&&((await this._unsub)(),this._unsub=void 0)}},{kind:"method",key:"_continue",value:function(){this._step++}},{kind:"method",key:"_stopNetwork",value:async function(){var e;this._stoppingNetwork=!0,await this._getNetworkStatus(),(null===(e=this._networkStatus)||void 0===e?void 0:e.state)!==c.N8?(this._unsub=this.hass.connection.subscribeEvents((()=>this._networkStopped()),"zwave.network_stop"),this.hass.callService("zwave","stop_network")):this._networkStopped()}},{kind:"method",key:"_setupZwaveJs",value:async function(){var e;const t=await(0,c.mB)(this.hass);(0,p.t)(this,{continueFlowId:t.flow_id,dialogClosedCallback:e=>{e.entryId&&(this._zwaveJsEntryId=e.entryId,this._getZwaveJSNodesStatus(),this._step=3)},showAdvanced:null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced}),this.hass.loadBackendTranslation("title","zwave_js",!0)}},{kind:"method",key:"_getZwaveJSNodesStatus",value:async function(){var e;if(null!==(e=this._nodeReadySubscriptions)&&void 0!==e&&e.length){(await Promise.all(this._nodeReadySubscriptions)).forEach((e=>{e()}))}this._nodeReadySubscriptions=[];const t=await(0,d.OV)(this.hass,this._zwaveJsEntryId),i=t.controller.nodes.map((e=>(0,d.mZ)(this.hass,this._zwaveJsEntryId,e))),r=(await Promise.all(i)).filter((e=>!e.ready));if(console.log("waiting for nodes to be ready",r),this._getMigrationData(),0===r.length)return void(this._waitingOnDevices=[]);this._nodeReadySubscriptions=r.map((e=>(0,d.M0)(this.hass,this._zwaveJsEntryId,e.node_id,(()=>{this._getZwaveJSNodesStatus()}))));const n=await(0,l._Y)(this.hass.connection);this._waitingOnDevices=n.filter((e=>{const i=(0,d.T5)(e);return!(!i||Number(i.home_id)!==t.controller.home_id)&&r.some((e=>i.node_id===e.node_id))}))}},{kind:"method",key:"_getMigrationData",value:async function(){try{this._migrationData=await(0,d.x1)(this.hass,this._zwaveJsEntryId,!0)}catch(e){return void(0,h.Ys)(this,{title:"Failed to get migration data!",text:"unknown_command"===e.code?"Restart Home Assistant and try again.":e.message})}this._migratedZwaveEntities=Object.keys(this._migrationData.migration_entity_map),Object.keys(this._migrationData.migration_device_map).length&&this._fetchDevices()}},{kind:"method",key:"_fetchDevices",value:function(){this._unsubDevices=(0,l.q4)(this.hass.connection,(e=>{if(!this._migrationData)return;const t=Object.keys(this._migrationData.migration_device_map),i={};e.forEach((e=>{t.includes(e.id)&&(i[e.id]=(0,l.jL)(e,this.hass))})),this._deviceNameLookup=i}))}},{kind:"method",key:"_doMigrate",value:async function(){(await(0,d.x1)(this.hass,this._zwaveJsEntryId,!1)).migrated?this._step=4:(0,h.Ys)(this,{title:"Migration failed!"})}},{kind:"method",key:"_networkStopped",value:function(){this._unsubscribe(),this._getMigrationConfig(),this._stoppingNetwork=!1,this._step=2}},{kind:"method",key:"_getNetworkStatus",value:async function(){this._networkStatus=await(0,c.HV)(this.hass)}},{kind:"get",static:!0,key:"styles",value:function(){return[u.Qx,r.iv`
        .content {
          margin-top: 24px;
        }

        .flex-container {
          display: flex;
          align-items: center;
        }

        .flex-container ha-circular-progress {
          margin-right: 20px;
        }

        blockquote {
          display: block;
          background-color: var(--secondary-background-color);
          color: var(--primary-text-color);
          padding: 8px;
          margin: 8px 0;
          font-size: 0.9em;
          font-family: monospace;
        }

        ha-card {
          margin: 0 auto;
          max-width: 600px;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=73135a11.js.map