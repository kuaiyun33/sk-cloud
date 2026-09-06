# 多语言检查命令

在仓库根执行。任一检查发现非法键、三语不一致、重复/相似、LANG 兜底或硬编码中文时，必须先修复后交付。未执行写原因。

## 键名合法性（含插件 lang）

```bash
php -r '$roots=["webman/public/template","webman/public/plugin","webman/resource/translations"]; $files=[]; foreach($roots as $root){$it=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root, FilesystemIterator::SKIP_DOTS)); foreach($it as $file){$path=$file->getPathname(); if(substr($path,-4)!==".php") continue; if(preg_match("#/(lang|translations)(/|$)#", $path)){ $files[]=$path; } }} sort($files); $invalid=[]; $check=function(array $array,string $file,string $prefix="") use (&$check,&$invalid){ foreach($array as $key=>$value){ if(is_string($key) && !preg_match("/^[a-z][a-z0-9_]*$/", $key)){ $invalid[]=[$file,$prefix.$key]; } if(is_array($value)){ $check($value,$file,$prefix.$key."."); } } }; foreach($files as $file){ $data=require $file; if(is_array($data)){ $check($data,$file); } } echo "files=".count($files)." invalid=".count($invalid).PHP_EOL; foreach($invalid as $item){ echo $item[0]." => ".$item[1].PHP_EOL; }'
```

## 调用处驼峰键

```bash
rg -n "_trans\\(\\s*['\"][A-Za-z0-9]*[A-Z][A-Za-z0-9_]*['\"]|trans\\(\\s*['\"][A-Za-z0-9]*[A-Z][A-Za-z0-9_]*['\"]|__\\(\\s*['\"][A-Za-z0-9]*[A-Z][A-Za-z0-9_]*['\"]" webman admin --glob '!**/vendor/**' --glob '!**/node_modules/**' --glob '!**/runtime/**'
rg -n "LANG\\?\\.[A-Za-z0-9]*[A-Z][A-Za-z0-9_]*|LANG\\.[A-Za-z0-9]*[A-Z][A-Za-z0-9_]*|\\$LANG\\.[A-Za-z0-9]*[A-Z][A-Za-z0-9_]*|LANG\\[['\"][A-Za-z0-9]*[A-Z][A-Za-z0-9_]*['\"]\\]|\\$LANG\\[['\"][A-Za-z0-9]*[A-Z][A-Za-z0-9_]*['\"]\\]" webman admin --glob '!**/vendor/**' --glob '!**/node_modules/**' --glob '!**/runtime/**'
```

## 三语键集合一致

同一作用域下 `zh-cn` / `zh-tw` / `en-us` 键集合必须完全一致。通用包、各主题 `lang`、系统 translations 分开比对。

```bash
php -r '$groups=["template/lang"=>"webman/public/template/lang","client"=>"webman/public/template/client/default/lang","buy"=>"webman/public/template/buy/default/lang","web"=>"webman/public/template/web/default/lang"]; foreach($groups as $name=>$root){ if(!is_dir($root)) continue; $locales=[]; foreach(glob($root."/*.php") as $file){ $data=require $file; if(is_array($data)){ $locales[basename($file,".php")]=array_keys($data);} } $base=null; foreach($locales as $locale=>$keys){ sort($keys); if($base===null){$base=$keys; continue;} $missing=array_values(array_diff($base,$keys)); $extra=array_values(array_diff($keys,$base)); if($missing||$extra){ echo $name." ".$locale." mismatch".PHP_EOL; if($missing) echo "missing=".implode(",",$missing).PHP_EOL; if($extra) echo "extra=".implode(",",$extra).PHP_EOL; } } } $t="webman/resource/translations"; if(is_dir($t)){ $locales=[]; foreach(["zh-cn","zh-tw","en-us"] as $locale){ $file=$t."/".$locale."/messages.php"; if(!is_file($file)) continue; $data=require $file; if(is_array($data)){ $locales[$locale]=array_keys($data);} } $base=null; foreach($locales as $locale=>$keys){ sort($keys); if($base===null){$base=$keys; continue;} $missing=array_values(array_diff($base,$keys)); $extra=array_values(array_diff($keys,$base)); if($missing||$extra){ echo "translations ".$locale." mismatch".PHP_EOL; if($missing) echo "missing=".implode(",",$missing).PHP_EOL; if($extra) echo "extra=".implode(",",$extra).PHP_EOL; } } }'
```

## 近义重复

```bash
php -r '$roots=["webman/public/template/lang","webman/public/template/client/default/lang"]; $map=[]; $norm=function($v){ $v=preg_replace("/%[a-z][a-z0-9_]*%/","%x%",(string)$v); $v=preg_replace("/[[:space:]，。！？、,.!?:：；;（）()【】\\[\\]《》<>\"'\''`~]+/u","",$v); return mb_strtolower($v,"UTF-8"); }; foreach($roots as $root){ foreach(glob($root."/*.php") as $file){ $locale=basename($file,".php"); $data=require $file; if(!is_array($data)) continue; foreach($data as $key=>$value){ if(!is_string($value)) continue; $n=$norm($value); if($n==="") continue; $map[$locale][$n][]=[$file,$key,$value]; } } } foreach($map as $locale=>$items){ foreach($items as $rows){ if(count($rows)<2) continue; echo "duplicate ".$locale.PHP_EOL; foreach($rows as $row){ echo $row[0]." => ".$row[1]." = ".$row[2].PHP_EOL; } } }'
```

## LANG 兜底与硬编码中文

```bash
rg -n "LANG\\.[a-z][a-z0-9_]*\\s*(\\|\\||\\?\\?)|LANG\\[['\"][a-z][a-z0-9_]*['\"]\\]\\s*(\\|\\||\\?\\?)|typeof\\s+LANG|typeof\\s+_trans" webman/public/template webman/public/resources --glob '!**/*.min.js'
rg -n "[\\x{4e00}-\\x{9fff}]" webman/public/template webman/public/resources --glob '*.html' --glob '*.js' --glob '!**/*.min.js'
```
