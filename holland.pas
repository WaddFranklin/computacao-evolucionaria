{
   Este é um programa do algoritmo genético de Holland
   para encontrar o número binário dentre do interválao de 
   [0,255] que apresenta a maior ocorrencia da sub string 
   01
   * a população é formada por 10 cromossomo 
   * o cromossomo é um vetor binário de 8 posições 
   * cruzamento de um ponto de corte e probabilidade de cruzamento maior que 60
   * mutação por complemento com probabilidade de mutação maior que 90
   * inversão com probabilidade de inversão de 90
   * seleção e substituição elitista 
}

Program Holland1;

type pop= array[1..10,1..8] of integer;
     adapt= array[1..10] of integer;
     des= array[1..30,1..8] of integer;
     adaptdes= array[1..30] of integer;

var pA: pop;
    dA: des;
    f: adapt;
    fdes: adaptdes;
    i,j: integer;
    tamD: integer;

procedure gera_pop_in(var p: pop);					// gera aleatoriamente a população inicial
begin
    for i:= 1 to 10 do								// laço do população
        for j:= 1 to 8 do							// laço do cromossomo
                p[i,j]:= random(2);
end;

procedure mostra_pop(p: pop);						// mostra a população atual
begin
    for i:= 1 to 10 do								// laço da população
        begin
            for j:= 1 to 8 do						// laço do cromossomo
                write(p[i,j]);						// escreve cada posição do cromossomo
            writeln;    							// salta de linha
        end;    
end;

procedure adaptacao(var f1: adapt; p: pop);			// calcula o valor da adaptação da população atual
begin
    for i:= 1 to 10 do								// laço do população
        begin										
            f1[i]:= 0;								// local onde a adaptação do cromossomo i será armazenada
            for j:= 1 to 7 do						// laço do cromossomo
                if (p[i,j]=0) and (p[i,j+1]=1)		// verifica a ocorrencia de 01 no veror
                then f1[i]:= f1[i] + 1;				// caso positivo incrementa o valor da adaptação
        end;    
end;

procedure mostra_pop_adapt(f1: adapt; p: pop); 		// mostra a população atual com sua adaptação
begin
    for i:= 1 to 10 do								// laço da população
        begin
            for j:= 1 to 8 do						// laço do cromossomo
                write(p[i,j]);					 	// escreve cada posição do cromossomo
            writeln('=', f1[i]);    				// escreve a adaptação do cromossomo e salta de linha	
        end;    
end;

procedure ordena_pop(var f1: adapt; var p: pop);	// algoritmo bolha de ordenação
var a,b,c: integer;
begin
    for a:= 1 to 9 do								// laço do primeiro ponteiro
        for b:= a+1 to 10 do						// laço do segundo pondeiro
            begin
                if (f1[a] < f1[b])
                then begin
                        for i:= 1 to 8 do			// troca os cromossomos na população
                            begin
                                c:= p[a,i];
                                p[a,i]:= p[b,i];
                                p[b,i]:= c;
                            end;
                        c:= f1[a];					// troca a adaptação
                        f1[a]:= f1[b];
                        f1[b]:= c;
                     end;
            end;
end;

procedure cruzamento(p: pop; var d: des; var tam: integer);		// cruzamento de 1 ponto de corte
var a,b,x,corte: integer;
begin
    for a:= 1 to 4 do											// laço do cromossomo pai
        for b:= (a + 1) to 5 do									// laço do cromossomo mãe
            begin
                x:= random(100) + 1;      						// probabilidade de cruzamento
                if (x>60) and (tam<=28)
                then begin
						corte:= random(8) + 1;				// geração do ponto de corte
														
						for x:= 1 to corte do				// copia a primeira parte da posição 1 até corte
							begin
								d[tam + 1,x]:= p[a,x];
                                d[tam + 2,x]:= p[b,x];
                            end;
                            
						for x:= corte + 1 to 8 do			// copia a segunda parte da posição corte+1 até 8
							begin
								d[tam + 1,x]:= p[b,x];
								d[tam + 2,x]:= p[a,x];
							end;
                                
						tam:= tam + 2;
                     end;
            end;
end;

procedure mostra_des(d: des;tam: integer);						// mostra a população de descendentes
begin
    for i:= 1 to tam do
        begin
            for j:= 1 to 8 do
                write(d[i,j]);
            writeln;    
        end;    
end;

procedure mutacao(p: pop; var d: des; var tam: integer);		// mutação por complemento
var a,b,x: integer;
begin
    for a:= 1 to 5 do											// laço do cromossomo a ser mutado
        begin
			x:= random(100) + 1;								// probabilidade de mutação
            if (tam <=29) and (x>90)
            then begin
                tam:= tam + 1;									
                for b:= 1 to 8 do
                    begin
                        x:= random(2) ;							// verifica se deve mutar a atual posição do cromossomo
                        if (x = 0)
                        then if (p[a,b] = 0)
                             then d[tam,b]:= 1
                             else d[tam,b]:= 0
                        else d[tam,b]:= p[a,b];
                    end;
            end;
        end;
end;

procedure inversao(p: pop; var d: des; var tam: integer);
var a,b,p1,p2,x,y: integer;
begin
    for a:= 1 to 5 do
        begin
            x:= random(100) + 1;									// probabilidade de inversão é maior do que 90
            if (x>90) and (tam<=29)				
            then begin
                    tam:= tam + 1;				
                    for b:= 1 to 8 do								// copia o cromossomo 
                        d[tam,b]:= p[a,b];

                    p1:= random(7) + 1;								// escolhe a primeira posição
                    p2:= random(8) + 1;						
                    while (p2<p1) do 								// escolhe a segunda posição, onde p1 < p2
						p2:= random(8) + 1;						
                    
					x:= (p2-p1) div 2;
					
                    for b:= 0 to x do								// inverte o conteúdo do cromossomo entre p1 e p2
                        begin
                            y:= d[tam, p1 + b];
                            d[tam, p1 + b]:= d[tam, p2 - b ];
                            d[tam, p2 - b]:= y;
                        end;
                 end;
        end;
end;

procedure adaptacaoD(var f2: adaptdes; d: des; tam: integer);
begin
    for i:= 1 to tam do
        begin
            f2[i]:= 0;
            for j:= 1 to 7 do
                if (d[i,j]=0) and (d[i,j+1]=1)
                then f2[i]:= f2[i] + 1;
        end;    
end;

procedure mostra_pop_adaptD(f2: adaptdes; d: des; tam: integer);
begin
    for i:= 1 to tam do
        begin
            for j:= 1 to 8 do
                write(d[i,j]);
            writeln('=', f2[i]);    
        end;    
end;

procedure ordena_popD(var f2: adaptdes; var d: des; tam: integer);		// oedenação de bolha
var a,b,c,x: integer;
begin
    for a:= 1 to tam - 1 do
        for b:= a + 1 to tam do
            begin
                if (f2[a] < f2[b])							
                then begin
                
                        for i:= 1 to 8 do								// troca cromossomo
                            begin
                                c:= d[a,i];
                                d[a,i]:= d[b,i];
                                d[b,i]:= c;
                            end;
                            
                        c:= f2[a];										// troca adaptação
                        f2[a]:= f2[b];
                        f2[b]:= c;
                        
                     end;
            end;
end;

procedure substituicao(var p: pop; d: des; var f1: adapt; f2: adaptdes; tam: integer);
var a,b,c,x: integer;
    pN: pop;
    f3: adaptdes;
begin
    b:= 1; 											// indice da população atual 
    c:= 1; 											// indice da população de descendentes
    for a:= 1 to 10 do 								// indice da nova população
        begin
  

			if (b<=10) and (c<=tam)  
			then 	if (f1[b] > f2[c])				// população é maior que descendente
					then begin 
                    		for i:= 1 to 8 do		// copia o cromossomo da população atual para a nova população
                        		pN[a,i]:= p[b,i];
                    		f3[a]:= f1[b];			// copia a adaptação desse cromossomo
                    		b:= b + 1;				// incrementa o indice da população atual
						 end
                    else begin
							for i:= 1 to 8 do		// copia o cromossomo da população de descendentes para a nova população
								pN[a,i]:= d[c,i];
							f3[a]:= f2[c];			// copia a adaptação desse cromossomo
							c:= c + 1;				// incrementa o indice da população de descendentes
						 end
						 
			else 	if (b<=10) and (c>tam)
					then begin 
							for i:= 1 to 8 do		// copia o cromossomo da população atual para a nova população
								pN[a,i]:= p[b,i];
                    		f3[a]:= f1[b];			// copia a adaptação desse cromossomo
                    		b:= b + 1;				// incrementa o indice da população atual
                 	      end
					else begin
							for i:= 1 to 8 do
								pN[a,i]:= d[c,i];
							f3[a]:= f2[c];
							c:= c + 1;
						 end    
        end;

    for a:= 1 to 10 do								// coloca a nova população no lugar da população atual
        begin
            for i:= 1 to 8 do
                p[a,i]:= pN[a,i];
            f1[a]:= f3[a];							// coloca a nova adaptação no lugar da adaptação atual
        end;    
end;

begin
  Randomize;
  
  writeln; writeln('população atual gerada');
  gera_pop_in(pA);
  mostra_pop(pA);
  
  writeln; writeln('população atual com sua adaptação');
  adaptacao(f,pA);
  mostra_pop_adapt(f,pA);
  
  writeln; writeln('população atual na ordem decrescente da adaptação');
  ordena_pop(f,pA);
  mostra_pop_adapt(f,pA);
  
  while (f[1]<>4) do
    begin
        {vou ficar com os 5 cromossomos mais adaptados, que são os 5 primeiros da minha população atual}
        
        tamD:= 0;
        
        writeln; writeln('cruzamento');
        cruzamento(pA,dA,tamD);
        mostra_des(dA,tamD);
        
        writeln; writeln('mutação');
        mutacao(pA,dA,tamD);
        mostra_des(dA,tamD);

        writeln; writeln('inversao');
        inversao(pA,dA,tamD);
        mostra_des(dA,tamD);

        writeln; writeln('população descencente com sua adaptação');
        adaptacaoD(fdes,dA,tamD);
        mostra_pop_adaptD(fdes,dA,tamD);
        
        writeln; writeln('população descendente na ordem decrescente da adaptação');
        ordena_popD(fdes,dA,tamD);
        mostra_pop_adaptD(fdes,dA,tamD);
        
        writeln; writeln('população nova');
        substituicao(pA,dA,f,fdes,tamD);
        mostra_pop_adapt(f,pA);
        
    end;

end.