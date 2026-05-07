import sys

file_path = r"c:\Users\tiago\OneDrive\Desktop\Mestre Clientes\Killprocess\gui.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Procura a linha específica do log com a indentação errada
    if 'def log(self, text, tag=None):' in line and i > 300 and i < 400:
        # Força a indentação correta (4 espaços para método de classe)
        new_lines.append("    def log(self, text, tag=None):\n")
        # Ajusta as linhas seguintes do método log
        j = i + 1
        while j < len(lines) and (lines[j].startswith("        ") or lines[j].strip() == ""):
            # Se a linha original tinha 8 espaços, agora deve ter 8 (manteve o corpo do método)
            # Mas espera, se o método estava com 4 espaços extras, o corpo estava com 12? 
            # Deixe-me ver o view_file anterior.
            # 375:     def log(self, text, tag=None):
            # Isso são 4 espaços. O corpo:
            # 376:         if tag:
            # Isso são 8 espaços. 
            # Se o def está com 4 espaços, ele já está no nível da classe!
            # ENTÃO POR QUE O TYPEERROR?
            # "TypeError: PremiumKillprocessApp.log() takes 2 positional arguments but 3 were given"
            # Se ele é um método de classe, self é passado.
            # Se eu chamo self.log("msg", "info"), self é 1, "msg" é 2, "info" é 3.
            # Se a definição é (self, text, tag=None), ele aceita 3 argumentos.
            
            # ESPERA! Se ele foi definido DENTRO de _build_terminal, o primeiro argumento "self" 
            # na verdade se refere ao "self" da classe externa capturado pela closure, 
            # MAS quando chamado como self.log, o python passa o objeto novamente.
            
            # Deixe-me ver o erro de novo:
            # "TypeError: PremiumKillprocessApp.log() takes 2 positional arguments but 3 were given"
            # Se o erro diz que ele toma 2 mas recebeu 3, e a assinatura é (self, text, tag=None), 
            # isso significa que o Python acha que tag NÃO existe ou que self NÃO é o primeiro.
            
            # Ah! Se ele foi definido como uma função normal (não método) mas com nome 'self':
            # def log(self, text, tag=None): ...
            # E se ele não estiver na classe, mas sim no escopo local.
            
            # Vou apenas reescrever o bloco inteiro garantindo 4 espaços no def e 8 no corpo.
            pass
        new_lines.append(line.replace("    def log", "    def log")) # Mantém como está se já tiver 4
    else:
        new_lines.append(line)

# Vou usar uma abordagem mais radical: ler o arquivo e substituir a string exata.
content = "".join(lines)
old_block = """    def log(self, text, tag=None):
        if tag:
            self.log_textbox.insert("end", text + "\\n", tag)
        else:
            self.log_textbox.insert("end", text + "\\n")
        self.log_textbox.see("end")"""

# Remove espaços extras se houver
content = content.replace(old_block, old_block.replace("    def log", "    def log"))

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Indentação corrigida.")
