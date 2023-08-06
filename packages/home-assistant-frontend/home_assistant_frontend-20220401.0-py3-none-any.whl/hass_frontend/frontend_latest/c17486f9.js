/*! For license information please see c17486f9.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8757],{63207:(t,e,i)=>{i(65660),i(15112);var s=i(9672),n=i(87156),r=i(50856),o=i(48175);(0,s.k)({_template:r.d`
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
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:o.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,n.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,n.vz)(this.root).appendChild(this._img))}})},89194:(t,e,i)=>{i(48175),i(65660),i(70019);var s=i(9672),n=i(50856);(0,s.k)({_template:n.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},21560:(t,e,i)=>{i.d(e,{ZH:()=>l,MT:()=>r,U2:()=>h,RV:()=>n,t8:()=>a});const s=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let t;return new Promise((e=>{const i=()=>indexedDB.databases().finally(e);t=setInterval(i,100),i()})).finally((()=>clearInterval(t)))};function n(t){return new Promise(((e,i)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>i(t.error)}))}function r(t,e){const i=s().then((()=>{const i=indexedDB.open(t);return i.onupgradeneeded=()=>i.result.createObjectStore(e),n(i)}));return(t,s)=>i.then((i=>s(i.transaction(e,t).objectStore(e))))}let o;function c(){return o||(o=r("keyval-store","keyval")),o}function h(t,e=c()){return e("readonly",(e=>n(e.get(t))))}function a(t,e,i=c()){return i("readwrite",(i=>(i.put(e,t),n(i.transaction))))}function l(t=c()){return t("readwrite",(t=>(t.clear(),n(t.transaction))))}},97330:(t,e,i)=>{i.d(e,{_:()=>n,B:()=>r});var s=i(43715);const n=(t,e,i,n)=>{if(t[e])return t[e];let r,o=0,c=(0,s.M)();const h=()=>{if(!i)throw new Error("Collection does not support refresh");return i(t).then((t=>c.setState(t,!0)))},a=()=>h().catch((e=>{if(t.connected)throw e}));return t[e]={get state(){return c.state},refresh:h,subscribe(e){o++,1===o&&(n&&(r=n(t,c)),i&&(t.addEventListener("ready",a),a()));const s=c.subscribe(e);return void 0!==c.state&&setTimeout((()=>e(c.state)),0),()=>{s(),o--,o||(r&&r.then((t=>{t()})),t.removeEventListener("ready",h))}}},t[e]},r=(t,e,i,s,r)=>n(s,t,e,i).subscribe(r)},43715:(t,e,i)=>{i.d(e,{M:()=>s});const s=t=>{let e=[];function i(i,s){t=s?i:Object.assign(Object.assign({},t),i);let n=e;for(let e=0;e<n.length;e++)n[e](t)}return{get state(){return t},action(e){function s(t){i(t,!1)}return function(){let i=[t];for(let t=0;t<arguments.length;t++)i.push(arguments[t]);let n=e.apply(this,i);if(null!=n)return n instanceof Promise?n.then(s):s(n)}},setState:i,subscribe:t=>(e.push(t),()=>{!function(t){let i=[];for(let s=0;s<e.length;s++)e[s]===t?t=null:i.push(e[s]);e=i}(t)})}}},19596:(t,e,i)=>{i.d(e,{s:()=>d});var s=i(81563),n=i(38941);const r=(t,e)=>{var i,s;const n=t._$AN;if(void 0===n)return!1;for(const t of n)null===(s=(i=t)._$AO)||void 0===s||s.call(i,e,!1),r(t,e);return!0},o=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},c=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),l(e)}};function h(t){void 0!==this._$AN?(o(this),this._$AM=t,c(this)):this._$AM=t}function a(t,e=!1,i=0){const s=this._$AH,n=this._$AN;if(void 0!==n&&0!==n.size)if(e)if(Array.isArray(s))for(let t=i;t<s.length;t++)r(s[t],!1),o(s[t]);else null!=s&&(r(s,!1),o(s));else r(this,t)}const l=t=>{var e,i,s,r;t.type==n.pX.CHILD&&(null!==(e=(s=t)._$AP)&&void 0!==e||(s._$AP=a),null!==(i=(r=t)._$AQ)&&void 0!==i||(r._$AQ=h))};class d extends n.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),c(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,s;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(s=this.disconnected)||void 0===s||s.call(this)),e&&(r(this,t),o(this))}setValue(t){if((0,s.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}},1460:(t,e,i)=>{i.d(e,{l:()=>o});var s=i(15304),n=i(38941);const r={},o=(0,n.XM)(class extends n.Xe{constructor(){super(...arguments),this.nt=r}render(t,e){return e()}update(t,[e,i]){if(Array.isArray(e)){if(Array.isArray(this.nt)&&this.nt.length===e.length&&e.every(((t,e)=>t===this.nt[e])))return s.Jb}else if(this.nt===e)return s.Jb;return this.nt=Array.isArray(e)?Array.from(e):e,this.render(e,i)}})},22142:(t,e,i)=>{i.d(e,{C:()=>d});var s=i(15304),n=i(38941),r=i(81563),o=i(19596);class c{constructor(t){this.U=t}disconnect(){this.U=void 0}reconnect(t){this.U=t}deref(){return this.U}}class h{constructor(){this.Y=void 0,this.q=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Y=this.q=void 0}}const a=t=>!(0,r.pt)(t)&&"function"==typeof t.then;class l extends o.s{constructor(){super(...arguments),this._$Cft=1073741823,this._$Cwt=[],this._$CG=new c(this),this._$CK=new h}render(...t){var e;return null!==(e=t.find((t=>!a(t))))&&void 0!==e?e:s.Jb}update(t,e){const i=this._$Cwt;let n=i.length;this._$Cwt=e;const r=this._$CG,o=this._$CK;this.isConnected||this.disconnected();for(let t=0;t<e.length&&!(t>this._$Cft);t++){const s=e[t];if(!a(s))return this._$Cft=t,s;t<n&&s===i[t]||(this._$Cft=1073741823,n=0,Promise.resolve(s).then((async t=>{for(;o.get();)await o.get();const e=r.deref();if(void 0!==e){const i=e._$Cwt.indexOf(s);i>-1&&i<e._$Cft&&(e._$Cft=i,e.setValue(t))}})))}return s.Jb}disconnected(){this._$CG.disconnect(),this._$CK.pause()}reconnected(){this._$CG.reconnect(this),this._$CK.resume()}}const d=(0,n.XM)(l)}}]);
//# sourceMappingURL=c17486f9.js.map