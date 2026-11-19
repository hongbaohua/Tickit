function _safeStr(s){return s.replace(/[^\p{L}\p{N}_]/gu,"_");}
function _getUnitName(filename){const m=filename.match(/Day\s*\d+/i);if(m)return m[0].replace(/\s+/g," ").trim();const stem=filename.replace(/\.md$/i,"");return stem.length>20?stem.slice(0,20):stem;}
function _makeId(t,u,n){return `${_safeStr(t)}__${_safeStr(u)}__${n}`;}
function _parseQuestionsBlock(block){const questions=[];const pattern=/^\s*(\d+)[.、\s]\s*/gm;const matches=[...block.matchAll(pattern)];const optionPattern=/^\s*\(([A-D])\)\s*(.*)/;
for(let i=0;i<matches.length;i++){const start=matches[i].index;const end=i+1<matches.length?matches[i+1].index:block.length;const chunk=block.slice(start,end).trim();const lines=chunk.split("\n");const number=parseInt(matches[i][1],10);const options={};let q=lines[0].replace(/^\s*\d+[.、\s]\s*/,"").trim();let found=false;
for(let j=1;j<lines.length;j++){const line=lines[j];const m=line.match(optionPattern);if(m){options[m[1]]=m[2].trim();found=true;}else if(!found&&line.trim()){q+=" "+line.trim();}}
if(q&&Object.keys(options).length>0)questions.push({number,question:q.replace(/\s+/g," ").trim(),options});}return questions;}
function _parseAnswersBlock(block){const answers={};const pattern=/^\s*(\d+)[.、\s]?\s*(?:\*\*)?\(([^)]+)\)(?:\*\*)?\s*(.*)/gm;const matches=[...block.matchAll(pattern)];
for(let i=0;i<matches.length;i++){const number=parseInt(matches[i][1],10);answers[number]={letter:matches[i][2].trim()};}return answers;}
function parseMarkdown(text,topic,filename){const regex=new RegExp(`(?:^|\\n)[#\\s\\-]*解答與詳細解析[#\\s\\-]*`,"i");const m=text.match(regex);if(!m)return null;
const qs=_parseQuestionsBlock(text.slice(0,m.index));const as=_parseAnswersBlock(text.slice(m.index+m[0].length));return {qs,as};}
const fs=require('fs');const dir='out_v2/華語領隊人員評量';const units=JSON.parse(fs.readFileSync('units_v2.json'));let bad=0,total=0;
for(const u of units){const t=fs.readFileSync(dir+'/'+u.file,'utf8');const r=parseMarkdown(t,'領隊人員評量',u.file);
 if(!r){console.log('NOSEP',u.file);bad++;continue;}
 const nums=r.qs.map(q=>q.number);const expect=[...Array(u.n).keys()].map(i=>i+1);
 const ok=JSON.stringify(nums)===JSON.stringify(expect)&&r.qs.every(q=>Object.keys(q.options).length===4)&&expect.every(n=>r.as[n]&&/^[ABCD]$/.test(r.as[n].letter));
 total+=r.qs.length; if(!ok){bad++;console.log('BAD',u.unit,nums.length,u.n, nums.filter((x,i)=>x!==i+1).slice(0,5));}
 if(_getUnitName(u.file)!==u.unit)console.log('UNITNAME',u.file);}
console.log('units',units.length,'bad',bad,'questions',total);
