Hi Wolfgang, Hi Jakob,
1. Code in deutsch kommentieren fühlt sich nicht richtig an, ich nehme englisch
2. Train_info.txt notiert alle Zuginfo, in für das Programm leserlicher Form. Das ist nötig, weil wir sonst von der Bahn nur ein Paar wenige züge bekommen.
3. Die File update_files.py setzt eine anfrage ab, und erweitert dann Train_info.txt um die neuen züge. Wenn duplikate entstehen wird das mit dem größeren delay behalten(das ist dann normalerweise aktueller, ich habe keine bessere Lösung gefunden)
4. Demnach sollten wir irgendwie update_files.py einige male laufen lassen(wenn du weißt wie alle 10 min 100 züge anfragen wäre zb. gut)
5. main.py stellt eine analyse Klasse, vielleicht kannst du dir da was nettes ausdenken

6. Wenn wir zu viele Züge anfragen bekommen wir einen Fehler! Wie viele züge gehen ist nicht konstant! ICh weiß nicht warum, vieleicht sollen wir versuchen diesen fehler zu fangen, und dann die zugzahl reduzieren. Letzteres heißt das argument von add_new_trains_to_file() zu reduzieren, bis es passt. Das zu implementieren steht noch aus!
