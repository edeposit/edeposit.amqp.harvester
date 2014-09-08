edeposit.amqp.harvester
=======================
Tento modul obsahuje funkce pro stahování metadat ze stránek několika vybraných vydavatelů. Momentálně jsou k dispozici programové komponenty pro webové prezentace nakladatelství `Ben <http://ben.cz>`_, `Grada <http://grada.cz>`_, `CPress <http://cpress.cz>`_ a `ZonerPress <http://zonerpress.cz>`_.

Použití modulu
--------------
Podobně jako ostatní prvky projektu Edeposit je i tento modul součástí asynchronního distribuovaného systému, jehož jednotlivé komponenty spolu komunikují přes AMQP protokol. O to se stará modul `edeposit.amqp <http://edeposit-amqp.readthedocs.org/>`_.

`edeposit.amqp.harvester` poskytuje pouze rozhraní umožňující sklízení metadat, nikoliv script, které získané informace předává dál. Ten je možné najít v modulu `edeposit.amqp <http://edeposit-amqp.readthedocs.org/>`_, kde se nachází pod názvem `edeposit_amqp_harvester.py <http://edeposit-amqp.readthedocs.org/en/latest/api/harvester.html>`_.

Spuštěním tohoto scriptu dochází k "sklizení" dat ze všech podporovaných komponent a jejich odeslání na AMQP. Data jsou odesílána ve formátu struktury :class:`.Publications`, která ve svém těle nese pole struktur :class:`.Publication` se sklizenými metadaty.

Testovací script
----------------


Testování modulu
----------------