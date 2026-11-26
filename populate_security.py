import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course, Module, Lesson

def run_security_batch_3():
    print("Cargando TANDA 3 FINAL: Módulo 5 de Ciberseguridad (Defensiva, WAF, Hardening y Respuesta)...")

    course = Course.objects.get(slug="introduccion-ciberseguridad-ofensiva-defensiva")

    # =========================================================================
    # MÓDULO 5: Ciberseguridad Defensiva y Endurecimiento (Hardening)
    # =========================================================================
    mod5, _ = Module.objects.update_or_create(
        course=course,
        order=5,
        defaults={'title': "Módulo 5: Ciberseguridad Defensiva y Endurecimiento (Hardening)"}
    )
    mod5.lessons.all().delete()

    # Lección 5.1 - HARDENING
    Lesson.objects.create(
        module=mod5,
        title="5.1 Endurecimiento de Sistemas (Hardening)",
        order=1,
        content="""
        <p class="text-base text-slate-700 leading-relaxed mb-4">
            El <strong>endurecimiento (hardening)</strong> consiste en asegurar un sistema operativo, servidor, base de datos o aplicación eliminando servicios innecesarios, cerrando puertos por defecto, aplicando los parches de actualización más recientes y configurando permisos estrictos para reducir al mínimo su superficie de ataque.
        </p>

        <div class="my-6 p-6 rounded-3xl bg-emerald-50 border-2 border-emerald-200 shadow-sm">
            <h4 class="font-bold text-emerald-950 text-sm mb-3">Principios Clave del Hardening:</h4>
            <ul class="list-disc pl-6 space-y-2 text-xs sm:text-sm text-slate-700 leading-relaxed">
                <li><strong>Deshabilitar lo que no se usa:</strong> Todo servicio, protocolo o puerto abierto que no tenga una justificación operativa debe desinstalarse o apagarse.</li>
                <li><strong>Cambio obligatorio de valores predeterminados:</strong> Reemplazar contraseñas de fábrica, puertos estándar (como cambiar SSH del puerto 22 a otro no predecible) y nombres de usuario 'admin' o 'root'.</li>
                <li><strong>Políticas de parches continuos:</strong> Aplicar actualizaciones de seguridad de forma automatizada para mitigar vulnerabilidades conocidas de día cero (Zero-Day).</li>
            </ul>
        </div>
        """
    )

    # Lección 5.2 - WAF Y SIEM
    Lesson.objects.create(
        module=mod5,
        title="5.2 Cortafuegos de Aplicaciones Web (WAF) y Monitoreo",
        order=2,
        content="""
        <p class="text-base text-slate-700 leading-relaxed mb-4">
            En una infraestructura defensiva moderna, la protección perimetral opera en dos frentes complementarios:
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
            <div class="p-6 bg-white border-2 border-indigo-200 rounded-3xl shadow-sm">
                <span class="block font-black text-indigo-950 text-base mb-2">WAF (Web Application Firewall)</span>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    Sistema de defensa ubicado entre los clientes y la aplicación web que <strong>analiza, filtra y bloquea patrones de tráfico malicioso conocidos</strong> (como ataques SQLi o XSS) antes de que lleguen al servidor de backend.
                </p>
            </div>

            <div class="p-6 bg-white border-2 border-sky-200 rounded-3xl shadow-sm">
                <span class="block font-black text-sky-950 text-base mb-2">SIEM / Monitoreo Centralizado</span>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    Herramientas de <strong>recopilación y análisis de registros (logs) en tiempo real</strong> para correlacionar eventos entre múltiples servidores y detectar anomalías o comportamientos sospechosos de intrusión.
                </p>
            </div>
        </div>
        """
    )

    # Lección 5.3 - SAST VS DAST
    Lesson.objects.create(
        module=mod5,
        title="5.3 Análisis Estático y Dinámico en CI/CD (SAST / DAST)",
        order=3,
        content="""
        <p class="text-base text-slate-700 leading-relaxed mb-4">
            La integración de seguridad dentro del ciclo de desarrollo (DevSecOps) automatiza la detección de fallas en dos etapas del pipeline:
        </p>

        <!-- DIAGRAMA PIPELINE SAST Y DAST -->
        <div class="my-8 p-6 bg-slate-50 border border-slate-200 rounded-3xl shadow-sm text-center">
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-6">Seguridad Automatizada en el Pipeline CI/CD</h4>
            
            <div class="grid grid-cols-1 sm:grid-cols-5 gap-3 text-xs font-bold items-center">
                <div class="p-4 bg-white border-2 border-slate-200 rounded-2xl shadow-xs">
                    Código Commit
                </div>

                <div class="text-slate-400 font-black text-xl rotate-90 sm:rotate-0">&rarr;</div>

                <div class="p-4 bg-indigo-50 border-2 border-indigo-300 text-indigo-950 rounded-2xl shadow-xs">
                    Build<br>
                    <span class="inline-block mt-1 px-2 py-0.5 bg-indigo-200 text-indigo-900 text-[10px] rounded-full">SAST (Estático)</span>
                </div>

                <div class="text-slate-400 font-black text-xl rotate-90 sm:rotate-0">&rarr;</div>

                <div class="p-4 bg-emerald-50 border-2 border-emerald-300 text-emerald-950 rounded-2xl shadow-xs">
                    Deploy / Runtime<br>
                    <span class="inline-block mt-1 px-2 py-0.5 bg-emerald-200 text-emerald-900 text-[10px] rounded-full">DAST (Dinámico)</span>
                </div>
            </div>
        </div>

        <div class="space-y-4 my-6">
            <div class="p-5 bg-white border border-gray-200 rounded-2xl shadow-xs">
                <strong class="text-indigo-950 block text-sm mb-1">SAST (Static Application Security Testing):</strong>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">Análisis estático del código fuente en busca de vulnerabilidades (contraseñas quemadas, funciones inseguras, falta de sanitización) <strong>antes de compilarlo</strong>.</p>
            </div>

            <div class="p-5 bg-white border border-gray-200 rounded-2xl shadow-xs">
                <strong class="text-emerald-950 block text-sm mb-1">DAST (Dynamic Application Security Testing):</strong>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">Análisis dinámico que evalúa la aplicación <strong>en ejecución</strong> simulando ataques externos automatizados desde la pipeline de CI/CD para encontrar fallas de configuración y lógica en vivo.</p>
            </div>
        </div>
        """
    )

    # Lección 5.4 - RESPUESTA A INCIDENTES
    Lesson.objects.create(
        module=mod5,
        title="5.4 Respuesta a Incidentes y Planes de Contingencia",
        order=4,
        content="""
        <p class="text-base text-slate-700 leading-relaxed mb-4">
            Procedimientos formales para contener, investigar, mitigar y recuperarse de una brecha de seguridad activa, minimizando el impacto operativo y asegurando la preservación de evidencias forenses.
        </p>

        <!-- DIAGRAMA CICLO RESPUESTA A INCIDENTES -->
        <div class="my-8 p-6 bg-slate-50 border border-slate-200 rounded-3xl shadow-sm text-center">
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-6">Ciclo de Vida de Respuesta a Incidentes</h4>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs font-bold">
                <div class="p-4 bg-white border-2 border-indigo-200 text-indigo-950 rounded-2xl shadow-xs">
                    <span class="block text-indigo-600 text-sm mb-1">1</span>
                    Preparación<br><span class="text-[10px] text-slate-500 font-normal">Planes, roles y herramientas</span>
                </div>
                <div class="p-4 bg-white border-2 border-amber-200 text-amber-950 rounded-2xl shadow-xs">
                    <span class="block text-amber-600 text-sm mb-1">2</span>
                    Detección y Análisis<br><span class="text-[10px] text-slate-500 font-normal">Confirmar el vector de ataque</span>
                </div>
                <div class="p-4 bg-white border-2 border-rose-200 text-rose-950 rounded-2xl shadow-xs">
                    <span class="block text-rose-600 text-sm mb-1">3</span>
                    Contención y Recuperación<br><span class="text-[10px] text-slate-500 font-normal">Aislar y restaurar servicios</span>
                </div>
                <div class="p-4 bg-white border-2 border-emerald-200 text-emerald-950 rounded-2xl shadow-xs">
                    <span class="block text-emerald-600 text-sm mb-1">4</span>
                    Actividad Post-Incidente<br><span class="text-[10px] text-slate-500 font-normal">Lecciones aprendidas</span>
                </div>
            </div>
        </div>
        """
    )

    # Lección 5.5 - PRÁCTICAS DEL MÓDULO 5
    Lesson.objects.create(
        module=mod5,
        title="5.5 Laboratorio Práctico del Módulo 5",
        order=5,
        content="""
        <p class="text-base text-slate-700 leading-relaxed mb-4">
            Ejercicios cortos para resolver en papel o en un editor de texto; no requieren instalar ni usar herramientas externas.
        </p>

        <div class="space-y-6 my-6">
            <!-- Práctica 5.1 -->
            <div class="p-5 bg-white border-2 border-slate-200 rounded-3xl shadow-xs">
                <strong class="text-slate-900 block text-sm mb-2">Práctica 5.1 – Checklist de hardening</strong>
                <p class="text-xs sm:text-sm text-slate-600 mb-2 leading-relaxed">
                    Marca cuáles de estas acciones son parte del endurecimiento de un servidor y cuáles no:
                </p>
                <ol class="list-decimal pl-5 space-y-1 text-xs sm:text-sm text-slate-700 mb-3">
                    <li>Desinstalar servicios que no se usan.</li>
                    <li>Cambiar las contraseñas que vienen por defecto.</li>
                    <li>Dejar todos los puertos abiertos "por si acaso".</li>
                    <li>Aplicar las actualizaciones de seguridad.</li>
                    <li>Dar permisos de administrador a todos los usuarios.</li>
                    <li>Restringir permisos de archivos solo a lo necesario.</li>
                </ol>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 text-xs text-emerald-950">
                    <strong>Resultado esperado:</strong> Son medidas legítimas de hardening: <strong>1, 2, 4 y 6</strong>. (Las opciones 3 y 5 aumentan la vulnerabilidad radicalmente).
                </div>
            </div>

            <!-- Práctica 5.2 -->
            <div class="p-5 bg-white border-2 border-slate-200 rounded-3xl shadow-xs">
                <strong class="text-slate-900 block text-sm mb-2">Práctica 5.2 – Lee un registro de accesos</strong>
                <p class="text-xs sm:text-sm text-slate-600 mb-2 leading-relaxed">
                    Revisa estas líneas de un registro (log) de ejemplo y señala cuáles deberían generar una alerta o regla de bloqueo en un WAF y por qué:
                </p>
                <code class="block bg-slate-900 text-slate-200 p-3 rounded-xl font-mono text-xs mb-3 space-y-1">
                    <div>192.0.2.10 GET /index.html 200</div>
                    <div>192.0.2.55 GET /buscar?q=zapatos 200</div>
                    <div class="text-rose-400">198.51.100.7 GET /buscar?q=' OR '1'='1 500</div>
                    <div class="text-amber-400">198.51.100.7 GET /buscar?q=&lt;script&gt;alert(1)&lt;/script&gt; 200</div>
                    <div class="text-purple-400">203.0.113.4 POST /login 401 (x40 en 1 minuto)</div>
                </code>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 text-xs text-emerald-950">
                    <strong>Resultado esperado:</strong> Líneas <strong>3 (posible SQLi)</strong>, <strong>4 (posible XSS)</strong> y <strong>5 (posible ataque de fuerza bruta por 40 fallos en un minuto)</strong>. Una regla de WAF debe bloquear IPs que envíen comillas no sanitizadas, etiquetas de script o exceso de peticiones 401.
                </div>
            </div>

            <!-- Práctica 5.3 -->
            <div class="p-5 bg-white border-2 border-slate-200 rounded-3xl shadow-xs">
                <strong class="text-slate-900 block text-sm mb-2">Práctica 5.3 – SAST o DAST, y encuentra fallas en el código</strong>
                <p class="text-xs sm:text-sm text-slate-600 mb-2 leading-relaxed">
                    Primero clasifica: (a) revisar el código antes de compilar buscando contraseñas escritas en él, (b) lanzar ataques simulados contra la app ya ejecutándose. Después encuentra 3 problemas de seguridad en este fragmento:
                </p>
                <code class="block bg-slate-900 text-slate-200 p-3 rounded-xl font-mono text-xs mb-3 space-y-1">
                    <div class="text-rose-400">clave_db = "admin123"</div>
                    <div class="text-amber-400">consulta = "SELECT * FROM notas WHERE id=" + id</div>
                    <div class="text-sky-400">hash = md5(contraseña)</div>
                </code>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 text-xs text-emerald-950">
                    <strong>Resultado esperado:</strong> (a) es <strong>SAST</strong> y (b) es <strong>DAST</strong>. Fallas en el código: 1) credencial quemada en el código fuente, 2) concatenación vulnerable a inyección SQL y 3) uso de hash obsoleto MD5 sin sal.
                </div>
            </div>

            <!-- Práctica 5.4 -->
            <div class="p-5 bg-white border-2 border-slate-200 rounded-3xl shadow-xs">
                <strong class="text-slate-900 block text-sm mb-2">Práctica 5.4 – Plan de respuesta a incidentes</strong>
                <p class="text-xs sm:text-sm text-slate-600 mb-2 leading-relaxed">
                    Supón que descubres que se filtró una base de datos con correos de usuarios. Ordena estos pasos: contener la brecha, recuperar el servicio, detectar y confirmar el incidente, preservar evidencia, notificar a los afectados, documentar lecciones aprendidas.
                </p>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 text-xs text-emerald-950">
                    <strong>Resultado esperado:</strong> Orden estricto: <strong>1. Detectar &rarr; 2. Contener &rarr; 3. Preservar evidencia forense &rarr; 4. Recuperar el servicio &rarr; 5. Notificar &rarr; 6. Documentar lecciones aprendidas</strong>.
                </div>
            </div>
        </div>
        """
    )

    # Examen 5.6
    Lesson.objects.create(
        module=mod5,
        title="5.6 Quiz del Módulo 5: Ciberseguridad Defensiva y Hardening",
        order=6,
        content="""
        <div class="mb-8 p-6 bg-slate-50 border border-gray-200 rounded-2xl">
            <span class="inline-block px-3 py-1 bg-emerald-100 text-tesoem-dark font-extrabold text-xs rounded-full uppercase tracking-wider mb-2">Examen de Módulo 5</span>
            <h3 class="text-lg font-bold text-slate-900 mb-1">Evaluación Final: Seguridad Defensiva y Respuesta</h3>
            <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                Selecciona la respuesta correcta para cada pregunta. Al terminar las 5 preguntas, haz clic en <strong>"Terminar y Calificar Examen"</strong> para obtener tu acreditación final del curso.
            </p>
        </div>

        <div class="space-y-6">
            <!-- P1 -->
            <div class="p-5 border border-gray-200 rounded-2xl bg-white shadow-sm">
                <p class="font-bold text-slate-800 text-sm mb-3">1. ¿En qué consiste el proceso de Endurecimiento (Hardening) de un servidor o aplicación?</p>
                <div class="space-y-2">
                    <button type="button" onclick="selectQuizOption(this, 1, false, 'Saturar la CPU es un ataque de denegación de servicio, no una práctica de seguridad.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">A) En aumentar deliberadamente la complejidad de las consultas SQL para saturar la CPU.</button>
                    <button type="button" onclick="selectQuizOption(this, 1, true, 'El hardening reduce la superficie de ataque cerrando brechas predeterminadas en configuraciones por defecto.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">B) En asegurar el sistema eliminando servicios innecesarios, cerrando puertos no utilizados, aplicando parches y configurando políticas estrictas de seguridad.</button>
                    <button type="button" onclick="selectQuizOption(this, 1, false, 'Deshabilitar respaldos destruye la disponibilidad y recuperación ante desastres.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">C) En deshabilitar los respaldos automáticos de base de datos.</button>
                    <button type="button" onclick="selectQuizOption(this, 1, false, 'Permitir acceso público a paneles de administración es una negligencia crítica.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">D) En permitir el acceso público sin restricciones a los paneles de administración.</button>
                </div>
                <div id="q_res_1" class="hidden mt-3 p-3 rounded-xl text-xs font-semibold"></div>
            </div>

            <!-- P2 -->
            <div class="p-5 border border-gray-200 rounded-2xl bg-white shadow-sm">
                <p class="font-bold text-slate-800 text-sm mb-3">2. ¿Cuál es el papel principal de un WAF (Web Application Firewall) en la arquitectura defensiva?</p>
                <div class="space-y-2">
                    <button type="button" onclick="selectQuizOption(this, 2, false, 'Un WAF es un escudo de red HTTP, no una base de datos.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">A) Funcionar como una base de datos relacional orientada a columnas.</button>
                    <button type="button" onclick="selectQuizOption(this, 2, true, 'Los WAF actúan como escudos perimetrales inteligentes analizando peticiones web entrantes en busca de ataques comunes.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">B) Inspeccionar, filtrar y bloquear tráfico HTTP malicioso (como ataques de inyección o XSS) antes de que alcance la aplicación de backend.</button>
                    <button type="button" onclick="selectQuizOption(this, 2, false, 'Las pruebas unitarias son ejecutadas por frameworks de desarrollo en CI/CD.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">C) Compilar automáticamente scripts de prueba unitaria en entornos locales.</button>
                    <button type="button" onclick="selectQuizOption(this, 2, false, 'El control de versiones es tarea exclusiva de Git.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">D) Gestionar el control de versiones distribuidas mediante Git.</button>
                </div>
                <div id="q_res_2" class="hidden mt-3 p-3 rounded-xl text-xs font-semibold"></div>
            </div>

            <!-- P3 -->
            <div class="p-5 border border-gray-200 rounded-2xl bg-white shadow-sm">
                <p class="font-bold text-slate-800 text-sm mb-3">3. ¿Qué diferencia clave existe entre las pruebas de seguridad SAST y DAST dentro de un pipeline de CI/CD?</p>
                <div class="space-y-2">
                    <button type="button" onclick="selectQuizOption(this, 3, true, 'SAST revisa el código fuente (estático) y DAST evalúa la app corriendo (dinámico), integrando seguridad automatizada en DevOps.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">A) SAST analiza el código estático sin ejecutarlo (código fuente), mientras que DAST analiza la aplicación en ejecución simulando ataques externos (caja negra).</button>
                    <button type="button" onclick="selectQuizOption(this, 3, false, 'No dependen de la tecnología de base de datos.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">B) SAST es exclusivo de bases de datos NoSQL y DAST de servidores físicos.</button>
                    <button type="button" onclick="selectQuizOption(this, 3, false, 'Ambas herramientas son ejecutadas de forma automatizada por la pipeline de CI/CD.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">C) SAST solo lo ejecutan usuarios externos y DAST los desarrolladores junior.</button>
                    <button type="button" onclick="selectQuizOption(this, 3, false, 'Poseen naturalezas de inspección opuestas: estática vs dinámica.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">D) No existe diferencia; ambos términos significan exactamente lo mismo.</button>
                </div>
                <div id="q_res_3" class="hidden mt-3 p-3 rounded-xl text-xs font-semibold"></div>
            </div>

            <!-- P4 -->
            <div class="p-5 border border-gray-200 rounded-2xl bg-white shadow-sm">
                <p class="font-bold text-slate-800 text-sm mb-3">4. ¿Qué objetivo persigue la implementación de herramientas de análisis de registros (Logs y SIEM) en una infraestructura corporativa?</p>
                <div class="space-y-2">
                    <button type="button" onclick="selectQuizOption(this, 4, false, 'Los logs se estructuran para optimizar almacenamiento y retención.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">A) Aumentar el consumo de almacenamiento en disco duro de manera innecesaria.</button>
                    <button type="button" onclick="selectQuizOption(this, 4, true, 'Los SIEM y logs centralizados permiten la detección temprana de anomalías e intentos de intrusión.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">B) Detectar en tiempo real anomalías, patrones sospechosos e indicios de actividades maliciosas o intrusiones.</button>
                    <button type="button" onclick="selectQuizOption(this, 4, false, 'SIEM complementa los firewalls; nunca los reemplaza.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">C) Reemplazar por completo el uso de firewalls perimetrales.</button>
                    <button type="button" onclick="selectQuizOption(this, 4, false, 'Los logs registran la actividad de red, no ocultan sintaxis de código.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">D) Ocultar los errores de sintaxis a los programadores.</button>
                </div>
                <div id="q_res_4" class="hidden mt-3 p-3 rounded-xl text-xs font-semibold"></div>
            </div>

            <!-- P5 -->
            <div class="p-5 border border-gray-200 rounded-2xl bg-white shadow-sm">
                <p class="font-bold text-slate-800 text-sm mb-3">5. ¿Por qué son vitales los procedimientos de Respuesta a Incidentes ante una brecha de seguridad confirmada?</p>
                <div class="space-y-2">
                    <button type="button" onclick="selectQuizOption(this, 5, false, 'El objetivo de la respuesta a incidentes es técnico y de remediación, no de culpabilidad.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">A) Para culpar públicamente a los clientes por el fallo del sistema.</button>
                    <button type="button" onclick="selectQuizOption(this, 5, true, 'Un plan de respuesta a incidentes estandariza la contención y recuperación ordenada ante ataques reales.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">B) Para contener el daño rápidamente, investigar el origen de la intrusión, mitigar la amenaza y restaurar la operación de forma segura.</button>
                    <button type="button" onclick="selectQuizOption(this, 5, false, 'Los respaldos son fundamentales para poder restaurar el servicio.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">C) Para evitar realizar respaldos de información en el futuro.</button>
                    <button type="button" onclick="selectQuizOption(this, 5, false, 'No implica cambiar de lenguaje en producción durante una crisis.')" class="w-full text-left p-3.5 text-sm bg-slate-50/50 border border-gray-200 rounded-xl hover:bg-slate-100 transition-all">D) Para forzar el cambio del lenguaje de programación del backend.</button>
                </div>
                <div id="q_res_5" class="hidden mt-3 p-3 rounded-xl text-xs font-semibold"></div>
            </div>
        </div>

        <div class="mt-10 pt-6 border-t border-gray-200 text-center">
            <div id="quizValidationWarning" class="hidden mb-4 p-3.5 bg-rose-50 border border-rose-200 text-rose-800 text-xs sm:text-sm font-bold rounded-xl animate-pulse"></div>
            <button type="button" id="btnSubmitExam" onclick="submitExam(5)" class="w-full sm:w-auto px-8 py-3.5 bg-tesoem-dark hover:bg-emerald-800 text-white font-extrabold text-sm sm:text-base rounded-2xl shadow-lg transition-all hover:scale-105 active:scale-95">
                Terminar y Calificar Examen 📝
            </button>
            <div id="quizScoreBox" class="hidden"></div>
        </div>
        """
    )

    print("¡CURSO 4 COMPLETO AL 100%! Los 5 Módulos de Ciberseguridad Ofensiva y Defensiva han sido cargados.")

if __name__ == '__main__':
    run_security_batch_3()