(this["webpackJsonptime-recorder-view"]=this["webpackJsonptime-recorder-view"]||[]).push([[0],{138:function(e,t,a){e.exports=a(177)},143:function(e,t,a){},177:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),c=a(11),l=a.n(c),i=(a(143),a(29)),o=a(37),m=a(9),u=a(104),s=a(215),d=a(211),E=a(213),g=a(50),f=a(214),h=a(42),p=a.n(h),b=a(99),k=a.n(b),v=a(52),_=a(35),y=a(100),O=a(101),j=a(111),w=new(function(e){function t(){var e;return Object(v.a)(this,t),(e=Object(y.a)(this,Object(O.a)(t).call(this))).authenticated=!1,e.accessToken="",e.user={},e}return Object(j.a)(t,e),Object(_.a)(t,[{key:"isAuthenticated",value:function(){return this.authenticated}},{key:"setAuthenticated",value:function(e){this.authenticated=e,this.emit("change")}},{key:"getAccessToken",value:function(){return this.accessToken}},{key:"setAccessToken",value:function(e){this.accessToken=e,this.emit("change")}},{key:"getUser",value:function(){return this.user}},{key:"setUser",value:function(e){this.user=e,this.emit("change")}}]),t}(a(102).EventEmitter)),C=a(103),N=a.n(C),S=a(18),A=a.n(S),x=a(238),D=a(239),T=Object(u.a)((function(e){return{root:{flexGrow:1},menuButton:{marginRight:e.spacing(2)},title:{flexGrow:1},slack:{width:32,height:32,marginRight:e.spacing(2)}}}));var F=function(){var e=T(),t=Object(n.useState)(!1),a=Object(m.a)(t,2),c=a[0],l=a[1],i=Object(n.useState)("error"),u=Object(m.a)(i,2),h=u[0],b=u[1],v=Object(n.useState)(""),_=Object(m.a)(v,2),y=_[0],O=_[1],j=Object(n.useState)(!1),C=Object(m.a)(j,2),S=C[0],F=C[1];Object(n.useEffect)((function(){w.on("change",(function(){l(w.isAuthenticated())}));var e=N.a.parse(window.location.search).code;void 0!==e&&A.a.get("https://slack.com/api/oauth.access",{params:{client_id:"3246745826.923685300119",client_secret:"0f959af4f1b0e43cd06a021d5390e188",code:e,redirect_uri:"https://baykraft-time-recorder.herokuapp.com/"}}).then((function(e){if(e.data.ok){var t=e.data.access_token,a=e.data.user_id;A.a.get("https://slack.com/api/users.info",{params:{token:t,user:a}}).then((function(e){e.data.ok?(w.setUser(e.data.user),w.setAccessToken(t),w.setAuthenticated(!0)):(b("error"),O(e.data.error),F(!0))})).catch((function(e){b("error"),O(e.message),F(!0)}))}else b("error"),O(e.data.error),F(!0)})).catch((function(e){b("error"),O(e.message),F(!0)}))}),[]);var M=function(e,t){"clickaway"!==t&&F(!1)};return c?r.a.createElement(o.a,{to:"/timerecord"}):r.a.createElement("div",{className:e.root},r.a.createElement(d.a,{position:"static"},r.a.createElement(E.a,null,r.a.createElement(f.a,{edge:"start",className:e.menuButton,color:"inherit","aria-label":"menu"},r.a.createElement(p.a,null)),r.a.createElement(g.a,{variant:"h6",className:e.title},"\u682a\u5f0f\u4f1a\u793e\u30d9\u30a4\u30af\u30e9\u30d5\u30c8"),r.a.createElement(s.a,{color:"inherit",onClick:function(){window.location="https://slack.com/oauth/authorize?client_id=".concat("3246745826.923685300119","&scope=users:read&redirect_uri=").concat("https://baykraft-time-recorder.herokuapp.com/")}},r.a.createElement("img",{src:k.a,className:e.slack,alt:"slack"}),"Login with Slack"))),r.a.createElement(D.a,{open:S,autoHideDuration:6e3,onClose:M},r.a.createElement(x.a,{severity:h,variant:"filled",onClose:M},y)))},M=a(2);function H(e){var t=e.children,a=Object(M.a)(e,["children"]),c=Object(n.useState)(w.isAuthenticated()),l=Object(m.a)(c,1)[0];return r.a.createElement(o.b,Object.assign({},a,{render:function(e){var a=e.location;return l?t:r.a.createElement(o.a,{to:{pathname:"/",state:{from:a}}})}}))}var P=a(227),B=a(232),R=a(230),V=a(226),Y=a(228),W=a(229),q=a(224),L=a(237),G=a(108),U=a.n(G),z=a(67),J=a.n(z),I=a(65),K=a.n(I),$=a(106),Q=a(240),X=a(66),Z=a.n(X),ee=a(68),te=a.n(ee),ae=a(241),ne=a(219),re=a(220),ce=a(221),le=a(222),ie=a(60),oe=a.n(ie),me=a(223),ue=a(59),se=a.n(ue),de=a(217),Ee=a(242),ge=a(243),fe=a(225),he=a(231),pe=Object(u.a)((function(e){return{root:{flexGrow:1},menuButton:{marginRight:e.spacing(2)},title:{flexGrow:1},userAvatar:{marginRight:e.spacing(2)},table:{"& .MuiTableCell-root":{whiteSpace:"nowrap"}},container:{marginTop:e.spacing(2),marginBottom:e.spacing(5)},tableToolbar:{"& .MuiTextField-root":{marginRight:e.spacing(2),marginLeft:e.spacing(1),width:100},"& .MuiIconButton-root":{marginLeft:e.spacing(2)},marginBottom:e.spacing(1)},disableCell:{backgroundColor:"#efefef"},holidayCell:{color:"#f44336",backgroundColor:"#efefef"},customerField:{width:50},dateField:{width:50},drawerList:{width:250}}})),be=["\u65e5","\u6708","\u706b","\u6c34","\u6728","\u91d1","\u571f"],ke={0:"",10:"\u6709\u4f11",11:"\u6709\u4f11(AM)",12:"\u6709\u4f11(PM)",20:"\u6b20\u52e4",21:"\u6b20\u52e4(AM)",22:"\u6b20\u52e4(PM)",30:"\u7279\u4f11",31:"\u7279\u4f11(AM)",32:"\u7279\u4f11(PM)",40:"\u4ee3\u4f11",41:"\u4ee3\u4f11(AM)",42:"\u4ee3\u4f11(PM)",50:"\u4f11\u51fa"};function ve(){var e=pe(),t=Object(n.useState)(w.getUser()),a=Object(m.a)(t,1)[0],c=Object(n.useState)((new Date).getFullYear()),l=Object(m.a)(c,2),o=l[0],u=l[1],h=Object(n.useState)((new Date).getMonth()+1),b=Object(m.a)(h,2),k=b[0],v=b[1],_=Object(n.useState)([]),y=Object(m.a)(_,2),O=y[0],j=y[1],C=Object(n.useState)("error"),N=Object(m.a)(C,2),S=N[0],T=N[1],F=Object(n.useState)(""),M=Object(m.a)(F,2),H=M[0],G=M[1],z=Object(n.useState)(!1),I=Object(m.a)(z,2),X=I[0],ee=I[1],ie=Object(n.useState)({}),ue=Object(m.a)(ie,2),ve=ue[0],_e=ue[1],ye=Object(n.useState)(!1),Oe=Object(m.a)(ye,2),je=Oe[0],we=Oe[1],Ce=Object(n.useState)(null),Ne=Object(m.a)(Ce,2),Se=Ne[0],Ae=Ne[1],xe=function(e,t,a,n,r,c,l,i,o,m,u,s,d){return{edit:e,id:t,year:a,month:n,date:r,day:c,holiday:l,customer:i,kind:o,start_time:m,end_time:u,total_time:s,note:d}},De=function(e){var t=0,a=0;return e.forEach((function(e){console.log(JSON.stringify(e)),e.total_time&&(t+=Number(e.total_time.split(":")[0]),a+=Number(e.total_time.split(":")[1]))})),(t+=a/60)+":"+("00"+(a%=60)).slice(-2)},Te=function(e,t){t.edit=!1,t.id=e.time_record_id,t.customer=e.customer,t.kind=e.kind,t.start_time=e.start_time,t.end_time=e.end_time,t.total_time=e.total_time,t.note=e.note},Fe=function(e){ve.hasOwnProperty(String(e.date))||(ve[String(e.date)]=Object.assign({},e))},Me=function(){for(var e=[],t=0,a=Object.entries(ke);t<a.length;t++){var n=a[t],c=Object(m.a)(n,2),l=c[0],i=c[1];e.push(r.a.createElement("option",{key:l,value:l},i))}return e},He=function(e,t){"clickaway"!==t&&ee(!1)},Pe=function(e,t){var a=new Date,n=e.split(":"),r=t.split(":");return new Date(a.getFullYear(),a.getMonth(),a.getDate(),Number(n[0]),Number(n[1]))<new Date(a.getFullYear(),a.getMonth(),a.getDate(),Number(r[0]),Number(r[1]))};return r.a.createElement("form",{className:e.root},r.a.createElement(de.a,null),r.a.createElement(d.a,{position:"sticky"},r.a.createElement(E.a,null,r.a.createElement(f.a,{edge:"start",className:e.menuButton,color:"inherit","aria-label":"menu",onClick:function(){return we(!0)}},r.a.createElement(p.a,null)),r.a.createElement(g.a,{variant:"h6",className:e.title},"\u682a\u5f0f\u4f1a\u793e\u30d9\u30a4\u30af\u30e9\u30d5\u30c8"),r.a.createElement(s.a,{color:"inherit"},r.a.createElement(Q.a,{alt:"avatar",src:a.profile.image_48,className:e.userAvatar}),a.profile.real_name))),r.a.createElement(ae.a,{open:je,onClose:function(){return we(!1)}},r.a.createElement("div",{className:e.drawerList,onClick:function(){return we(!1)},onKeyDown:function(){return we(!1)}},r.a.createElement(ne.a,{component:"nav"},r.a.createElement(re.a,{button:!0,component:i.b,to:"/timerecord"},r.a.createElement(ce.a,null,r.a.createElement(se.a,null)),r.a.createElement(le.a,{primary:"\u52e4\u6020\u8a18\u9332"})),r.a.createElement(me.a,null),r.a.createElement(re.a,{button:!0,component:i.b,to:"/breaktime"},r.a.createElement(ce.a,null,r.a.createElement(oe.a,null)),r.a.createElement(le.a,{primary:"\u4f11\u61a9\u6642\u9593\u8a2d\u5b9a"}))))),r.a.createElement(D.a,{open:X,autoHideDuration:6e3,onClose:He},r.a.createElement(x.a,{severity:S,variant:"filled",onClose:He},H)),r.a.createElement(q.a,{maxWidth:"lg",className:e.container},r.a.createElement(E.a,{className:e.tableToolbar},r.a.createElement(g.a,{variant:"h6",className:e.title},"\u52e4\u6020\u8a18\u9332"),r.a.createElement(L.a,{required:!0,label:"\u5e74",margin:"normal",defaultValue:o,onChange:function(e){return u(e.target.value)}}),r.a.createElement(fe.a,{required:!0,margin:"normal"},r.a.createElement(ge.a,{htmlFor:"select-month"},"\u6708"),r.a.createElement($.a,{value:k,inputProps:{id:"select-month"},onChange:function(e){return v(e.target.value)}},r.a.createElement((function(){for(var e=[],t=1;t<=12;t++)e.push(r.a.createElement("option",{key:t,value:t},t));return e}),null))),r.a.createElement(Ee.a,{title:"\u691c\u7d22"},r.a.createElement(f.a,{onClick:function(){return o?Number(o)<2020||Number(o)>(new Date).getFullYear()?(T("error"),G("\u5e74\u306f\u300c2020\u2266\u5165\u529b\u5e74\u2266\u73fe\u5728\u5e74\u300d\u306e\u7bc4\u56f2\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void ee(!0)):void A.a.get("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/time_records/").concat(o,"/").concat(k),{params:{token:w.getAccessToken()}}).then((function(e){A.a.get("https://holidays-jp.github.io/api/v1/".concat(o,"/date.json")).then((function(t){for(var a=e.data.records,n=t.data,r=new Date(o,k-1,1),c=[],l=function(){var e=r.getDate(),t=r.getDay(),l="".concat(o,"-").concat(("0"+k).slice(-2),"-").concat(("0"+e).slice(-2)),i=0===t||6===t||l in n?"H":"",m=a.find((function(t){return t.date===e}));if(m?c.push(xe(!1,m.time_record_id,o,k,e,be[t],i,m.customer,m.kind,m.start_time,m.end_time,m.total_time,m.note)):c.push(xe(!1,0,o,k,e,be[t],i,"",0,"","","",n[l])),r.setDate(e+1),Number(k)!==r.getMonth()+1)return"break"};;){if("break"===l())break}Ae(De(c)),j(c),_e({})})).catch((function(e){T("error"),G(e.message),ee(!0)}))})).catch((function(e){T("error"),G(e.message),ee(!0)})):(T("error"),G("\u5e74\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void ee(!0))}},r.a.createElement(U.a,null)))),r.a.createElement(V.a,null,r.a.createElement(P.a,{className:e.table,"aria-label":"timerecords",size:"small"},r.a.createElement(Y.a,null,r.a.createElement(W.a,null,r.a.createElement(R.a,{align:"center",scope:"row"},"\u65e5\u4ed8"),r.a.createElement(R.a,{align:"center"},"\u66dc\u65e5"),r.a.createElement(R.a,{align:"center"},"\u4f11\u65e5"),r.a.createElement(R.a,{align:"center"},"\u5ba2\u5148"),r.a.createElement(R.a,{align:"center"},"\u52e4\u4f11"),r.a.createElement(R.a,{align:"center"},"\u59cb\u696d"),r.a.createElement(R.a,{align:"center"},"\u7d42\u696d"),r.a.createElement(R.a,{align:"center"},"\u5408\u8a08"),r.a.createElement(R.a,{align:"center"},"\u5099\u8003"),r.a.createElement(R.a,{align:"center"},"\u64cd\u4f5c"))),r.a.createElement(he.a,null,r.a.createElement(W.a,null,r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,{align:"center"},"\u52b4\u50cd\u7d2f\u8a08"),r.a.createElement(R.a,null),r.a.createElement(R.a,null)),r.a.createElement(W.a,null,r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,null),r.a.createElement(R.a,{align:"center"},Se),r.a.createElement(R.a,null),r.a.createElement(R.a,null))),r.a.createElement(B.a,null,O.map((function(t){return r.a.createElement(W.a,{key:t.date},r.a.createElement(R.a,{align:"center",className:e.disableCell},t.date),r.a.createElement(R.a,{align:"center",className:e.disableCell},t.day),r.a.createElement(R.a,{align:"center",className:e.holidayCell},t.holiday),r.a.createElement(R.a,{align:"center"},t.edit?r.a.createElement(L.a,{defaultValue:t.customer,className:e.customerField,inputProps:{style:{textAlign:"center"}},autoFocus:!0,onChange:function(e){return function(e,t){Fe(e),e.customer=t,j(O.slice())}(t,e.target.value)}}):r.a.createElement("span",null,t.customer)),r.a.createElement(R.a,{align:"center"},t.edit?r.a.createElement($.a,{value:t.kind,onChange:function(e){return function(e,t){Fe(e),e.kind=t,j(O.slice())}(t,e.target.value)}},r.a.createElement(Me,null)):r.a.createElement("span",null,ke[t.kind])),r.a.createElement(R.a,{align:"center"},t.edit?r.a.createElement(L.a,{defaultValue:t.start_time,className:e.dateField,inputProps:{style:{textAlign:"center"}},onChange:function(e){return function(e,t){Fe(e),e.start_time=t,j(O.slice())}(t,e.target.value)}}):r.a.createElement("span",null,t.start_time)),r.a.createElement(R.a,{align:"center"},t.edit?r.a.createElement(L.a,{defaultValue:t.end_time,className:e.dateField,inputProps:{style:{textAlign:"center"}},onChange:function(e){return function(e,t){Fe(e),e.end_time=t,j(O.slice())}(t,e.target.value)}}):r.a.createElement("span",null,t.end_time)),r.a.createElement(R.a,{align:"center",className:e.disableCell},t.total_time),r.a.createElement(R.a,null,t.edit?r.a.createElement(L.a,{defaultValue:t.note,onChange:function(e){return function(e,t){Fe(e),e.note=t,j(O.slice())}(t,e.target.value)}}):r.a.createElement("span",null,t.note)),r.a.createElement(R.a,{align:"center"},t.edit?r.a.createElement("div",null,r.a.createElement(f.a,{"aria-label":"done",onClick:function(){return function(e){var t=RegExp(/\d{1,2}:\d{1,2}/);if(e.start_time&&!t.test(e.start_time))return T("error"),G("\u59cb\u696d\u306f\u300cHH:mm\u300d\u5f62\u5f0f\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void ee(!0);if(e.end_time&&!t.test(e.end_time))return T("error"),G("\u7d42\u696d\u306f\u300cHH:mm\u300d\u5f62\u5f0f\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void ee(!0);if(!Pe(e.start_time,e.end_time))return T("error"),G("\u59cb\u696d\u306f\u7d42\u696d\u3088\u308a\u3082\u524d\u306e\u6642\u9593\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void ee(!0);var a=e.year,n=e.month,r=e.date;0===e.id?A.a.post("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/time_records/").concat(a,"/").concat(n,"/").concat(r),{customer:e.customer,kind:e.kind,start_time:e.start_time,end_time:e.end_time,note:e.note},{params:{token:w.getAccessToken()}}).then((function(t){Te(t.data.record,e),Ae(De(O)),j(O.slice()),T("success"),G("\u66f4\u65b0\u3057\u307e\u3057\u305f\u3002"),ee(!0)})).catch((function(e){T("error"),G(e.message),ee(!0)})):A.a.put("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/time_records/").concat(a,"/").concat(n,"/").concat(r),{customer:e.customer,kind:e.kind,start_time:e.start_time,end_time:e.end_time,note:e.note},{params:{token:w.getAccessToken()}}).then((function(t){Te(t.data.record,e),Ae(De(O)),j(O.slice()),T("success"),G("\u66f4\u65b0\u3057\u307e\u3057\u305f\u3002"),ee(!0)})).catch((function(e){T("error"),G(e.message),ee(!0)}))}(t)}},r.a.createElement(K.a,null)),r.a.createElement(f.a,{"aria-label":"cancel",onClick:function(){return function(e){var t=ve[String(e.date)];t&&(e.customer=t.customer,e.kind=t.kind,e.start_time=t.start_time,e.end_time=t.end_time,e.total_time=t.total_time,e.note=t.note,delete ve[String(e.date)],_e(ve)),e.edit=!1,j(O.slice())}(t)}},r.a.createElement(Z.a,null))):r.a.createElement("div",null,r.a.createElement(f.a,{"aria-label":"edit",onClick:function(){return function(e){delete ve[String(e.date)],_e(ve),e.edit=!0,j(O.slice())}(t)}},r.a.createElement(J.a,null)),r.a.createElement(f.a,{"aria-label":"delete",onClick:function(){return function(e){var t=e.year,a=e.month,n=e.date;A.a.delete("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/time_records/").concat(t,"/").concat(a,"/").concat(n),{params:{token:w.getAccessToken()}}).then((function(){e.id=0,e.customer=null,e.kind=0,e.start_time=null,e.end_time=null,e.total_time=null,e.note=null,Ae(De(O)),j(O.slice()),T("success"),G("\u524a\u9664\u3057\u307e\u3057\u305f\u3002"),ee(!0)})).catch((function(e){T("error"),G(e.message),ee(!0)}))}(t)}},r.a.createElement(te.a,null)))))})))))))}var _e=a(109),ye=a.n(_e),Oe=a(233),je=a(234),we=a(235),Ce=a(236),Ne=a(110),Se=a.n(Ne),Ae=Object(u.a)((function(e){return{root:{flexGrow:1},menuButton:{marginRight:e.spacing(2)},title:{flexGrow:1},userAvatar:{marginRight:e.spacing(2)},drawerList:{width:250},container:{marginTop:e.spacing(2),marginBottom:e.spacing(2)},tableToolbar:{marginBottom:e.spacing(1)},table:{"& .MuiTableCell-root":{whiteSpace:"nowrap","& .MuiTextField-root":{width:100}}}}}));function xe(){var e=Ae(),t=Object(n.useState)(w.getUser()),a=Object(m.a)(t,1)[0],c=Object(n.useState)(!1),l=Object(m.a)(c,2),o=l[0],u=l[1],h=Object(n.useState)([]),b=Object(m.a)(h,2),k=b[0],v=b[1],_=Object(n.useState)({}),y=Object(m.a)(_,2),O=y[0],j=y[1],C=Object(n.useState)(!1),N=Object(m.a)(C,2),S=N[0],T=N[1],F=Object(n.useState)("2020"),M=Object(m.a)(F,2),H=M[0],G=M[1],U=Object(n.useState)("1"),z=Object(m.a)(U,2),I=z[0],X=z[1],ee=Object(n.useState)(""),ie=Object(m.a)(ee,2),ue=ie[0],he=ie[1],pe=Object(n.useState)(""),be=Object(m.a)(pe,2),ke=be[0],ve=be[1],_e=Object(n.useState)(""),Ne=Object(m.a)(_e,2),xe=Ne[0],De=Ne[1],Te=Object(n.useState)("error"),Fe=Object(m.a)(Te,2),Me=Fe[0],He=Fe[1],Pe=Object(n.useState)(""),Be=Object(m.a)(Pe,2),Re=Be[0],Ve=Be[1],Ye=Object(n.useState)(!1),We=Object(m.a)(Ye,2),qe=We[0],Le=We[1],Ge=function(e,t,a,n,r,c,l){return{edit:e,id:t,year:a,month:n,customer:r,start_time:c,end_time:l}};Object(n.useEffect)((function(){A.a.get("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/break_times"),{params:{token:w.getAccessToken()}}).then((function(e){var t=e.data.records.map((function(e){return Ge(!1,e.break_time_id,e.year,e.month,e.customer,e.start_time,e.end_time)}));v(t)})).catch((function(e){He("error"),Ve(e.message),Le(!0)}))}),[]);var Ue=function(e){O.hasOwnProperty(String(e.id))||(O[String(e.id)]=Object.assign({},e))},ze=function(){for(var e=[],t=1;t<=12;t++)e.push(r.a.createElement("option",{key:t,value:t},t));return e},Je=function(e,t){"clickaway"!==t&&Le(!1)},Ie=function(e,t){var a=new Date,n=e.split(":"),r=t.split(":");return new Date(a.getFullYear(),a.getMonth(),a.getDate(),Number(n[0]),Number(n[1]))<new Date(a.getFullYear(),a.getMonth(),a.getDate(),Number(r[0]),Number(r[1]))};return r.a.createElement("form",{className:e.root},r.a.createElement(de.a,null),r.a.createElement(d.a,{position:"sticky"},r.a.createElement(E.a,null,r.a.createElement(f.a,{edge:"start",className:e.menuButton,color:"inherit","aria-label":"menu",onClick:function(){return u(!0)}},r.a.createElement(p.a,null)),r.a.createElement(g.a,{variant:"h6",className:e.title},"\u682a\u5f0f\u4f1a\u793e\u30d9\u30a4\u30af\u30e9\u30d5\u30c8"),r.a.createElement(s.a,{color:"inherit"},r.a.createElement(Q.a,{alt:"avatar",src:a.profile.image_48,className:e.userAvatar}),a.profile.real_name))),r.a.createElement(ae.a,{open:o,onClose:function(){return u(!1)}},r.a.createElement("div",{className:e.drawerList,onClick:function(){return u(!1)},onKeyDown:function(){return u(!1)}},r.a.createElement(ne.a,{component:"nav"},r.a.createElement(re.a,{button:!0,component:i.b,to:"/timerecord"},r.a.createElement(ce.a,null,r.a.createElement(se.a,null)),r.a.createElement(le.a,{primary:"\u52e4\u6020\u8a18\u9332"})),r.a.createElement(me.a,null),r.a.createElement(re.a,{button:!0,component:i.b,to:"/breaktime"},r.a.createElement(ce.a,null,r.a.createElement(oe.a,null)),r.a.createElement(le.a,{primary:"\u4f11\u61a9\u6642\u9593\u8a2d\u5b9a"}))))),r.a.createElement(Oe.a,{open:S,onClose:function(){return T(!1)}},r.a.createElement(je.a,null,"\u4f11\u61a9\u6642\u9593\u8ffd\u52a0"),r.a.createElement(we.a,null,r.a.createElement(L.a,{label:"\u5e74",fullWidth:!0,required:!0,margin:"dense",defaultValue:H,onChange:function(e){return G(e.target.value)}}),r.a.createElement(fe.a,{required:!0,margin:"dense"},r.a.createElement(ge.a,{htmlFor:"select-month"},"\u6708"),r.a.createElement($.a,{value:I,inputProps:{id:"select-month"},onChange:function(e){return X(e.target.value)}},r.a.createElement(ze,null))),r.a.createElement(L.a,{autoFocus:!0,label:"\u5ba2\u5148",fullWidth:!0,required:!0,margin:"dense",onChange:function(e){return he(e.target.value)}}),r.a.createElement(L.a,{label:"\u958b\u59cb\u6642\u9593",fullWidth:!0,required:!0,margin:"dense",onChange:function(e){return ve(e.target.value)}}),r.a.createElement(L.a,{label:"\u7d42\u4e86\u6642\u9593",fullWidth:!0,required:!0,margin:"dense",onChange:function(e){return De(e.target.value)}})),r.a.createElement(Ce.a,null,r.a.createElement(s.a,{onClick:function(){T(!1)},color:"primary"},"\u30ad\u30e3\u30f3\u30bb\u30eb"),r.a.createElement(s.a,{onClick:function(){if(!H)return He("error"),Ve("\u5e74\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);if(!ue)return He("error"),Ve("\u5ba2\u5148\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);if(Number(H)<2020||Number(H)>(new Date).getFullYear())return He("error"),Ve("\u5e74\u306f\u300c2020\u2266\u5165\u529b\u5e74\u2266\u73fe\u5728\u5e74\u300d\u306e\u7bc4\u56f2\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0);if(!ke)return He("error"),Ve("\u958b\u59cb\u6642\u9593\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);if(!xe)return He("error"),Ve("\u7d42\u4e86\u6642\u9593\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);var e=RegExp(/\d{1,2}:\d{1,2}/);return e.test(ke)?e.test(xe)?Ie(ke,xe)?void A.a.post("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/break_times"),{year:H,month:I,customer:ue,start_time:ke,end_time:xe},{params:{token:w.getAccessToken()}}).then((function(e){var t=e.data.record,a=Ge(!1,t.break_time_id,t.year,t.month,t.customer,t.start_time,t.end_time);k.push(a),v(k.slice()),T(!1),He("success"),Ve("\u4f11\u61a9\u6642\u9593\u3092\u8ffd\u52a0\u3057\u307e\u3057\u305f\u3002"),Le(!0)})).catch((function(e){He("error"),Ve(e.message),Le(!0)})):(He("error"),Ve("\u958b\u59cb\u6642\u9593\u306f\u7d42\u4e86\u6642\u9593\u3088\u308a\u3082\u524d\u306e\u6642\u9593\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0)):(He("error"),Ve("\u7d42\u4e86\u6642\u9593\u306f\u300cHH:mm\u300d\u5f62\u5f0f\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0)):(He("error"),Ve("\u958b\u59cb\u6642\u9593\u306f\u300cHH:mm\u300d\u5f62\u5f0f\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0))},color:"primary"},"\u8ffd\u52a0"))),r.a.createElement(D.a,{open:qe,autoHideDuration:6e3,onClose:Je},r.a.createElement(x.a,{severity:Me,variant:"filled",onClose:Je},Re)),r.a.createElement(q.a,{maxWidth:"lg",className:e.container},r.a.createElement(E.a,{className:e.tableToolbar},r.a.createElement(g.a,{variant:"h6",className:e.title},"\u4f11\u61a9\u6642\u9593\u8a2d\u5b9a"),r.a.createElement(Ee.a,{title:"\u8ffd\u52a0"},r.a.createElement(f.a,{onClick:function(){var e=new Date;G(String(e.getFullYear())),X(String(e.getMonth()+1)),he(""),ve(""),De(""),T(!0)}},r.a.createElement(ye.a,null))),r.a.createElement(Ee.a,{title:"\u30ea\u30ed\u30fc\u30c9"},r.a.createElement(f.a,{onClick:function(){A.a.get("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/break_times"),{params:{token:w.getAccessToken()}}).then((function(e){var t=e.data.records.map((function(e){return Ge(!1,e.break_time_id,e.year,e.month,e.customer,e.start_time,e.end_time)}));v(t)})).catch((function(e){He("error"),Ve(e.message),Le(!0)}))}},r.a.createElement(Se.a,null)))),r.a.createElement(V.a,null,r.a.createElement(P.a,{size:"small",className:e.table,"aria-label":"breaktime"},r.a.createElement(Y.a,null,r.a.createElement(W.a,null,r.a.createElement(R.a,{align:"center"},"\u5e74"),r.a.createElement(R.a,{align:"center"},"\u6708"),r.a.createElement(R.a,{align:"center"},"\u5ba2\u5148"),r.a.createElement(R.a,{align:"center"},"\u958b\u59cb\u6642\u9593"),r.a.createElement(R.a,{align:"center"},"\u7d42\u4e86\u6642\u9593"),r.a.createElement(R.a,{align:"center"},"\u64cd\u4f5c"))),r.a.createElement(B.a,null,k.map((function(e){return r.a.createElement(W.a,{key:e.id},r.a.createElement(R.a,{align:"center"},e.edit?r.a.createElement(L.a,{defaultValue:e.year,inputProps:{style:{textAlign:"center"}},onChange:function(t){return function(e,t){Ue(e),e.year=t,v(k.slice())}(e,t.target.value)}}):r.a.createElement("span",null,e.year)),r.a.createElement(R.a,{align:"center"},e.edit?r.a.createElement($.a,{value:e.month,onChange:function(t){return function(e,t){Ue(e),e.month=t,v(k.slice())}(e,t.target.value)}},r.a.createElement(ze,null)):r.a.createElement("span",null,e.month)),r.a.createElement(R.a,{align:"center"},e.edit?r.a.createElement(L.a,{defaultValue:e.customer,inputProps:{style:{textAlign:"center"}},autoFocus:!0,onChange:function(t){return function(e,t){Ue(e),e.customer=t,v(k.slice())}(e,t.target.value)}}):r.a.createElement("span",null,e.customer)),r.a.createElement(R.a,{align:"center"},e.edit?r.a.createElement(L.a,{defaultValue:e.start_time,inputProps:{style:{textAlign:"center"}},onChange:function(t){return function(e,t){Ue(e),e.start_time=t,v(k.slice())}(e,t.target.value)}}):r.a.createElement("span",null,e.start_time)),r.a.createElement(R.a,{align:"center"},e.edit?r.a.createElement(L.a,{defaultValue:e.end_time,inputProps:{style:{textAlign:"center"}},onChange:function(t){return function(e,t){Ue(e),e.end_time=t,v(k.slice())}(e,t.target.value)}}):r.a.createElement("span",null,e.end_time)),r.a.createElement(R.a,{align:"center"},e.edit?r.a.createElement("div",null,r.a.createElement(f.a,{"aria-label":"done",onClick:function(){return function(e){if(!e.year)return He("error"),Ve("\u5e74\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);if(!e.customer)return He("error"),Ve("\u5ba2\u5148\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);if(Number(e.year)<2020||Number(e.year)>(new Date).getFullYear())return He("error"),Ve("\u5e74\u306f\u300c2020\u2266\u5165\u529b\u5e74\u2266\u73fe\u5728\u5e74\u300d\u306e\u7bc4\u56f2\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0);if(!e.start_time)return He("error"),Ve("\u958b\u59cb\u6642\u9593\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);if(!e.end_time)return He("error"),Ve("\u7d42\u4e86\u6642\u9593\u304c\u5165\u529b\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"),void Le(!0);var t=RegExp(/\d{1,2}:\d{1,2}/);return t.test(e.start_time)?t.test(e.end_time)?Ie(e.start_time,e.end_time)?void A.a.put("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/break_times/").concat(e.id),{year:e.year,month:e.month,customer:e.customer,start_time:e.start_time,end_time:e.end_time},{params:{token:w.getAccessToken()}}).then((function(t){var a=t.data.record;e.edit=!1,e.year=a.year,e.month=a.month,e.customer=a.customer,e.start_time=a.start_time,e.end_time=a.end_time,v(k.slice()),He("success"),Ve("\u66f4\u65b0\u3057\u307e\u3057\u305f\u3002"),Le(!0)})).catch((function(e){He("error"),Ve(e.message),Le(!0)})):(He("error"),Ve("\u958b\u59cb\u6642\u9593\u306f\u7d42\u4e86\u6642\u9593\u3088\u308a\u3082\u524d\u306e\u6642\u9593\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0)):(He("error"),Ve("\u7d42\u4e86\u6642\u9593\u306f\u300cHH:mm\u300d\u5f62\u5f0f\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0)):(He("error"),Ve("\u958b\u59cb\u6642\u9593\u306f\u300cHH:mm\u300d\u5f62\u5f0f\u3067\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"),void Le(!0))}(e)}},r.a.createElement(K.a,null)),r.a.createElement(f.a,{"aria-label":"cancel",onClick:function(){return function(e){var t=O[String(e.id)];t&&(e.customer=t.customer,e.start_time=t.start_time,e.end_time=t.end_time,delete O[String(e.id)],j(O)),e.edit=!1,v(k.slice())}(e)}},r.a.createElement(Z.a,null))):r.a.createElement("div",null,r.a.createElement(f.a,{"aria-label":"edit",onClick:function(){return function(e){delete O[String(e.id)],j(O),e.edit=!0,v(k.slice())}(e)}},r.a.createElement(J.a,null)),r.a.createElement(f.a,{"aria-label":"delete",onClick:function(){return function(e){A.a.delete("".concat("https://baykraft-time-recorder.herokuapp.com/rest","/break_times/").concat(e.id),{params:{token:w.getAccessToken()}}).then((function(){delete k[k.indexOf(e)],v(k.slice()),He("success"),Ve("\u524a\u9664\u3057\u307e\u3057\u305f\u3002"),Le(!0)})).catch((function(e){He("error"),Ve(e.message),Le(!0)}))}(e)}},r.a.createElement(te.a,null)))))})))))))}Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));l.a.render(r.a.createElement((function(){return r.a.createElement(i.a,null,r.a.createElement(o.d,null,r.a.createElement(o.b,{exact:!0,path:"/"},r.a.createElement(F,null)),r.a.createElement(H,{exact:!0,path:"/timerecord"},r.a.createElement(ve,null)),r.a.createElement(H,{exact:!0,path:"/breaktime"},r.a.createElement(xe,null)),r.a.createElement(o.b,{path:"*"},r.a.createElement(F,null))))}),null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))},99:function(e,t,a){e.exports=a.p+"static/media/slack_icon.be396144.svg"}},[[138,1,2]]]);
//# sourceMappingURL=main.1302c1f6.chunk.js.map