<script>
(function(){var io='IntersectionObserver'in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);e.target.querySelectorAll('[data-c]').forEach(cnt);if(e.target.dataset.c)cnt(e.target)}})},{rootMargin:'0px 0px -6% 0px'}):null;
document.querySelectorAll('.rv').forEach(function(el){io?io.observe(el):el.classList.add('in')});
function cnt(b){var n=+b.dataset.c,t0=performance.now();(function f(t){var p=Math.min(1,(t-t0)/1300);p=1-Math.pow(1-p,3);b.textContent=Math.round(n*p).toLocaleString('en');if(p<1)requestAnimationFrame(f)})(t0)}
var T=document.querySelectorAll('.ftabs button'),PN=document.querySelectorAll('.fp'),IND=document.getElementById('ind'),PR=document.getElementById('fprog'),cur=0,auto=true,t0=performance.now(),DUR=5200;
function show(n){cur=n;T.forEach(function(b,k){b.setAttribute('aria-selected',k===n)});PN.forEach(function(p,k){p.classList.toggle('on',k===n)});IND.style.transform='translateX('+(n*100)+'%)';t0=performance.now()}
T.forEach(function(b,k){b.addEventListener('click',function(){auto=false;PR.style.width='0';show(k)})});
var fz=document.querySelector('.fpanes'),sx=null;fz.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});fz.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;sx=null;if(Math.abs(dx)>40){auto=false;PR.style.width='0';show((cur+(dx<0?1:4))%5)}},{passive:true});
(function loop(t){if(auto){var p=(t-t0)/DUR;if(p>=1){show((cur+1)%5);p=0}PR.style.width=(p*100)+'%'}requestAnimationFrame(loop)})(performance.now());
var F=document.getElementById('fab'),H=document.querySelector('.hero .btns');addEventListener('scroll',function(){var r=H.getBoundingClientRect();F.classList.toggle('on',r.bottom<0&&document.querySelector('.end').getBoundingClientRect().top>innerHeight)},{passive:true});
document.querySelectorAll('.stats b[data-c]').forEach(function(b){b.closest('.rv')&&0})})();
</script>