import StdCTLextension
StdCTLextension.Input()
StdCTLextension.Print("www")
prompt = {'print':['In Print:Function(args)...Use to Output','33'],' in ':['is keyword in!!!!!!','34']}
highlight = {'+':35,'-':35,'%':35,'=':31,'*':35,'\\':35,'/':35,
'(':34,')':34,'[':34,']':34,'{':34,'}':34,'"':32,"'":32,':':32,'>':32,'<':32,
'|':35,'.':35,'~':35,'%':35,'^':35}
key = {' to ':'35'}
a = StdCTLextension.Input('prompt>',highlight=highlight,promptText=prompt,key=key)
StdCTLextension.Print(a,color='33')
StdCTLextension.Input()
