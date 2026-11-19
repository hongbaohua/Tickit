function _getUnitName(f){const m=f.match(/Day\s*\d+/i);if(m)return m[0];const s=f.replace(/\.md$/i,"");return s.length>20?s.slice(0,20):s;}
const u=JSON.parse(require('fs').readFileSync('units_v2.json'));const names=u.map(x=>_getUnitName(x.file));console.log(names, new Set(names).size===names.length);
