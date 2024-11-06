import streamlit as st
from streamlit_theme import st_theme
import numpy as np
import uproot # for reading .root files
import awkward as ak # for handling complex and nested data structures efficiently
import pandas as pd
from utils_analysis import *
from PIL import Image
import base64
import os
import json
import random
import time

                
def run(selected_language):
    # Initialize everything needed
    # Initialize flags to keep track of each step
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    if 'nlepton_cut_applied' not in st.session_state:
        st.session_state.nlepton_cut_applied = False

    if 'leptontype_cut_applied' not in st.session_state:
        st.session_state.leptontype_cut_applied = False

    if 'leptoncharge_cut_applied' not in st.session_state:
        st.session_state.leptoncharge_cut_applied = False

    if 'leptonpt_cut_applied' not in st.session_state:
        st.session_state.leptonpt_cut_applied = False

    if 'invariant_mass_calculated' not in st.session_state:
        st.session_state.invariant_mass_calculated = False
    
    if 'mc_loaded' not in st.session_state:
        st.session_state.mc_loaded = False

    # Initialize a special session state variable for the selectbox
    # This is so that the first cut option resets when using the reset analysis button
    if 'n_leptons_selection' not in st.session_state:
        st.session_state['n_leptons_selection'] = "--"

    # Initilize the expanders for the quizzes
    # First time they are expanded, when reseting they are not
    if 'expand_all' not in st.session_state:
        st.session_state['expand_all'] = True

    # Initialize session state for hint on lepton cut
    if 'show_hint' not in st.session_state:
        st.session_state['show_hint'] = False

    # Define a function to toggle the hint
    def toggle_hint():
        st.session_state['show_hint'] = not st.session_state['show_hint']

    if 'is_higgs' not in st.session_state:
        st.session_state['is_higgs'] = False

    if 'is_z' not in st.session_state:
        st.session_state['is_z'] = False

    # Get the current theme using st_theme
    theme = st_theme()

    # This is the json with all the info for all analyses
    # Build the path to the JSON file
    json_file_path = os.path.join('analyses', 'event_counts.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        analyses = json.load(json_file)


    ################ HERE IS WERE THE APP STARTS ################
    st.title("¡Descubre el Bosón Z y el Bosón de Higgs tú mismo!")

    # Introduction
    st.markdown("""
    Con esta aplicación interactiva podrás descubrir los bosones Z y de Higgs.
    ¡Comprendiendo y seleccionando eventos descubrirás las partículas tú mismo!
    """)

    st.markdown("## ¿Cuántos datos quieres utilizar?")
    st.markdown("""Comience su análisis eligiendo la cantidad de datos con los que desea trabajar. Utilice el control deslizante a continuación para seleccionar la **luminosidad integrada**, que es una medida de la cantidad de datos que ha recopilado el detector ATLAS.

Cuantos más datos analice, más posibilidades tendrá de detectar eventos raros como el bosón de Higgs. Pero tenga en cuenta que *más datos también pueden significar más tiempo de procesamiento*.""")    
    # Create a slider for luminosity
    lumi = st.slider(
        'Seleccionar luminosidad (fb$^{-1}$):', 
        min_value=12, 
        max_value=36, 
        step=12, 
        value=12
    )

    if st.button("Carga los datos"):
        # Reset the steps, so that people cannot break it clicking again
        # Reset info for the events
        if st.session_state.nlepton_cut_applied:
            # Reset flags
            st.session_state.nlepton_cut_applied = False
            st.session_state.leptontype_cut_applied = False
            st.session_state.leptoncharge_cut_applied = False
            st.session_state.invariant_mass_calculated = False
            st.session_state.mc_loaded = False
            st.session_state.is_z = False
            st.session_state.is_higgs = False

            # Delete the widget keys from session_state
            for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                if key in st.session_state:
                    del st.session_state[key]
        
        # Reading the data
        random_sleep = random.randint(1, lumi)
        # Display a spinner with the loading message
        with st.spinner("Cargando datos... Por favor espere."):
            # Simulate a time-consuming process with a random sleep
            time.sleep(random_sleep)

        st.session_state.data_loaded = True
        st.toast('¡Datos cargados exitosamente!', icon='📈')
        
    if st.session_state.data_loaded:
        st.info(f" Número inicial de eventos: {analyses[f'{lumi}']['nEvents']}")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Entendiendo la luminosidad")
            st.markdown(f"Seleccionaste una luminosidad de **{lumi} fb⁻¹**. Pero, ¿qué representa realmente la luminosidad integrada en un experimento de física de partículas?")

            possible = ['La cantidad de tiempo que el detector está activo',
                        'La cantidad de colisiones por segundo',
                        'Una medida de la cantidad total de colisiones durante un período de tiempo',
                        'La energía a la que ocurren las colisiones']
            answer = st.radio("Elige tu respuesta:", possible, index=None)

            if answer == possible[2]:
                st.success("¡Correcto! La luminosidad representa el número total de colisiones en el conjunto de datos. Cuanto mayor sea la luminosidad, mayores serán las posibilidades de observar eventos raros como el bosón de Higgs")
            elif answer:
                st.error("Incorrecto. ¡Inténtelo de nuevo o lea más sobre luminosidad!")

        # Using a selectbox to let users choose between amounts of leptons
        st.markdown("## Número de leptones en el estado final")
        st.markdown("En los colisionadores de partículas, cuando se produce una partícula, puede decaer inmediatamente en otras partículas, que se detectan y analizan. Al identificar todas las partículas en el estado final, podemos inferir qué partículas se crearon inicialmente durante la colisión. Un ejemplo es el número de leptones en el estado final, ya que diferentes procesos producen diferentes cantidades de leptones.")
        st.markdown("Below is a Feynman diagram showing a typical process that results in a final state with two leptons:")
        # Diagram for Z decay
        image_zdecay = f"images/Z_decay_{theme['base']}.png"
        # Encode the image in base64
        with open(image_zdecay, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        # Display the image centered and resizable using HTML with CSS
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_string}" alt="Centered Image" 
                    style="width: 50%; max-width: 500px; height: auto;">
                <figcaption style="font-size: 0.9em; color: gray;">El bosón Z decae a dos leptones.</figcaption>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("Decaimientos más complejas pueden implicar más leptones en el estado final")
        # Diagram for H decay
        image_zdecay = f"images/higgs4l_decay_{theme['base']}.png"
        # Encode the image in base64
        with open(image_zdecay, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        # Display the image centered and resizable using HTML with CSS
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_string}" alt="Centered Image" 
                    style="width: 50%; max-width: 500px; height: auto;">
                <figcaption style="font-size: 0.9em; color: gray;">El bosón de Higgs decae a bosones Z y, posteriormente, a leptones.</figcaption>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("A continuación se puede ver el recuento de leptones en todo el conjunto de datos. Notamos que, en general, es más común tener menos leptones en un evento")
        # Get the appropriate plot file based on the theme
        st.image(f"images/lepton_plot_{theme['base']}_{lumi}.png")

        st.markdown("Estudia los diagramas y los datos, y selecciona cuántos leptones esperas observar en tu estado final dependiendo del análisis que estés haciendo: encontrar el bosón Z o el bosón de Higgs.")
        
        st.warning("""
        Estás a punto de seleccionar la cantidad de leptones que deseas en tus datos. Sin embargo, es importante tener en cuenta que hemos agregado criterios adicionales para garantizar la calidad de estos leptones:

        - **Aislamiento:** cada leptón debe estar aislado, lo que significa que no está agrupado con otras partículas. Esto garantiza que nos estamos centrando en los leptones que probablemente se originaron directamente de la partícula que nos interesa, en lugar de interacciones de fondo.
        - **Niveles de identificación:** los leptones deben cumplir con criterios de identificación específicos para confirmar su tipo con alta confianza. La reconstrucción de partículas es compleja, por lo que tenemos diferentes niveles de identificación para mayor certeza. Por ejemplo, los muones deben pasar un nivel de identificación medio, mientras que los electrones solo necesitan pasar un nivel de identificación flexible, ya que los electrones son más fáciles de detectar.
        - **Condiciones de trigger:** los triggers son criterios establecidos para capturar eventos con ciertas características, lo que permite guardar solo los eventos que queremos analizar. Aquí, utilizamos triggers de electrones y muones para seleccionar eventos con señales significativas, refinando el conjunto de datos para aumentar las posibilidades de observar partículas que decaen a leptones o muones.

        Estos criterios ayudan a "limpiar" los datos, mejorando nuestras posibilidades de observar partículas como los bosones Z y Higgs.
        """)

        # Define the options
        n_leptons_options = ("--", 2, 3, 4)

        # Create the selectbox
        n_leptons = st.selectbox(
            '¿Cuántos leptones esperas en el estado final?',
            n_leptons_options,
            index=0,  # Default index for "--"
            key='n_leptons_selection'
        )

        # Access the selected value from session_state
        n_leptons = st.session_state['n_leptons_selection']

        if n_leptons == 2:
            st.success("""Has elegido un estado final con **2 leptones**.
                        Esto sugiere que te interesa un proceso en el que una única partícula intermedia deca a un par de leptones.
                        Los pares de leptones son comunes en muchas interacciones de partículas, especialmente cuando se consideran intermediarios neutros""")
        elif n_leptons == 4:
            st.success("""Estás viendo **4 leptones** en el estado final.
                        Esto a menudo indica una cadena de decaimientos, donde múltiples partículas intermedias decae a pares de leptones.
                        Estos escenarios son interesantes para estudiar interacciones complejas""")
        elif n_leptons != '--':
            st.warning("""Tener un número impar de leptones es inusual en procesos de desintegración simples, ya que los leptones suelen producirse en pares debido a las leyes de conservación.
                        Sin embargo, esto podría sugerir que estás explorando modos de desintegración más exóticos. ¿Estás buscando materia oscura?""")

        # Number of leptons button
        # We define a variable to avoid the page breaking when clicked more than once
        if st.button("Aplicar selección por número de leptones"):
            if st.session_state.nlepton_cut_applied:
                st.toast("Ya aplicaste una selección. Para reiniciar el análisis ve al final de la página.", icon='❌')
            elif n_leptons != '--':
                random_sleep = random.randint(1, round(lumi/3))
                # Display a spinner with the loading message
                with st.spinner("Seleccionando eventos... Por favor espere."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                st.session_state.nlepton_cut_applied = True
                st.toast("Selección aplicada exitosamente.", icon='✂️')
            else:
                st.error("Seleccione un número válido de leptones.")

    # Step 2: Dynamically generate selection for lepton flavors
    if st.session_state.nlepton_cut_applied:
        st.info(f"Eventos luego de la selección: {analyses[f'{lumi}'][f'{n_leptons}leptons']['nEvents']}")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Estado final de Leptones")
            st.markdown(f"""
            ¿Qué puede indicar el número de leptones?
            """)

            possible_lepton = ['Dos leptones indican una desintegración simple de una partícula neutra, como un bosón Z',
                            'Cuatro leptones indican una cadena de desintegración más compleja, que posiblemente involucre a un bosón de Higgs',
                            'Un número impar de leptones sugiere un proceso exótico',
                            'Todas las anteriores']
            answer_lepton = st.radio("Elige tu respuesta:", possible_lepton, index=None, key="lepton_selection_quiz")

            if answer_lepton == possible_lepton[3]:
                st.success("¡Correcto! Cada opción representa una posibilidad en función de tu selección.")
            elif answer_lepton:
                st.error("Incorrecto. Intenta pensar en cómo se producen los leptones en pares.")

        st.markdown("## Garanticemos la conservación")
        st.markdown("En las interacciones entre partículas, ciertas propiedades siempre se conservan, como la *carga* y el *sabor* leptónico. Comprender estas leyes de conservación ayuda a reducir las posibilidades de las partículas que están involucradas en el estado final.")
        st.markdown("En tu análisis, puedes ver el 'sabor' de los leptones (es decir, si son electrones o muones) y su carga (positiva o negativa). Las partículas con carga opuesta se llaman antipartículas, un electron positivo se llama positron y un muón positivo, anti-muón. El plot siguiente muestra la distribución del sabor de los leptones, con una barra para leptones cargados positivamente y otra para leptones cargados negativamente. Esto ayuda a identificar si el estado final obedece reglas de conservación.")
        
        # Display the pre-generated plot based on the theme
        st.image(f"images/lepton_barplot_{theme['base']}_{lumi}.png")
        
        st.markdown("Con esto en mente, realicemos la siguiente selección. Si no estás seguro, vuelve a ver los diagramas de Feynmann que están arriba. Puede que en ellos encuentres información que te pueda ayudar.")

        flavor_options = ["--", 'Mismo', 'Diferente']
        flavor = st.selectbox(f'¿Deberían los pares de leptones tener el mismo o diferente sabor?', flavor_options, key=f"flavor_selection")

        if flavor == 'Mismo':
            flavor = 'Same' #! Como arreglar esto para los diferentes idiomas
            st.success("""
                    Seleccionar dos leptones del mismo sabor significa que estás considerando escenarios donde las propiedades de los leptones son idénticas, 
                    como dos electrones o dos muones. Pares del mismo sabor se presentan en escenarios donde los decaimientos producto de la interacción entre 
                    partículas respeta la conservación de sabor.
                    """)
            
        elif flavor!= '--':
            flavor = 'Different'
            st.warning("""
                    Escoger leptones de diferentes sabores indica que estás examinando una situación donde los leptones no son idénticos, como un electrón y un muón.
                    Mientras esto puede ocurrir en algunos procesos, es menos común en decaimientos simples debido a las leyes de conservación de sabor.
                    """)
            
        # Apply lepton type cut based on flavor selection
        if st.button("Aplica selección de tipo de leptones"):
            if st.session_state.leptontype_cut_applied:
                st.toast("Ya aplicaste una selección. Para reiniciar el análisis ve al final de la página.", icon='❌')
            elif flavor != '--':    
                # Display a spinner with the loading message
                random_sleep = random.randint(1, round(lumi/3))
                with st.spinner("Seleccionando eventos... Por favor espere."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)

                # Display the cut result
                st.session_state.leptontype_cut_applied = True
                st.toast("Selección aplicada exitosamente.", icon='✂️')

            else:
                st.error("Selecciona una opción para el sabor de los leptones")

    # Step 3: Dynamically generate selection for lepton charges
    if st.session_state.leptontype_cut_applied:
        st.info(f"Eventos luego de la selección: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}']['nEvents']}")

        # Offer options for charge pairing: Same charge or Opposite charge
        charge_pair_options = ["--",'Igual', 'Opuesta']
        charge = st.selectbox('¿Deberían los pares de leptones tener la carga igual o contraria?', charge_pair_options)

        # Define the condition for the charge mask based on the selection
        if charge == 'Igual':
            charge = 'Same'
            st.warning("""Pares de leptones con la misma carga son inusuales porque usualmente la carga se conserva en las interacciones.
                    Sin embargo, algunos procesos más exótico, o identificación erronea puede resultar en pares con igual cargaa.
                    """)
        elif charge != '--':
            charge = 'Opposite'
            st.success("""Haz escogido leptones con carga opuesta. La mayoría de las interacciones conservan la carga,
                    por lo que es usual ver producción conjunta de un lepton y su antiparticulaso, resultando en cargas opuestas.
                    """)

            # Apply lepton type cut based on flavor selection
        if st.button("Apply lepton charge selection"):
            if st.session_state.leptoncharge_cut_applied:
                st.toast("Ya aplicaste una selección. Para reiniciar el análisis ve al final de la página.", icon='❌')
            elif charge != '--':
                # Display a spinner with the loading message
                random_sleep = random.randint(1, round(lumi/3))
                with st.spinner("Seleccionando eventos... Por favor espere."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                    st.session_state.leptoncharge_cut_applied = True

                    # Provide feedback to the user
                    st.toast("Selección aplicada exitosamente.", icon='✂️')
            else:
                st.error("Selecciona una opción para la carga de los leptones.")

        if st.session_state.leptoncharge_cut_applied:
            st.info(f"Eventos luego de la selección: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['nEvents']}")

        
            with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
                st.markdown("##### ⁉️ Entendiendo la Selección de Carga")
                st.markdown(f"""
                Seleccionaste pares de leptones con **carga {charge}**. ¿Por qué es la carga de los leptones importante en física de partículas?
                """)
                possible_charge = [
                    'La conservación de la carga es un principio fundamental y los productos de decaimientos deberían conservar la carga',
                    'Leptones con la misma carga son más comunes en decaimientos de partículas como el decaimiento del bosón Z',
                    'La carga no juega un rol importante en las interacciones de particulas',
                    'Pares de leptones de la misma carga indican colisiones altamente energéticas'
                ]
                
                answer_charge = st.radio("Elige tu respuesta:", 
                                        possible_charge, 
                                        index=None, key="charge_selection_quiz")

                # Checking for the correct answer and giving feedback
                if answer_charge == possible_charge[0]:
                    st.success("¡Correcto! La conservación de la carga es un fundamental en la física de partículas, y leptones de cargas opuestas son típicos en decaimientos como los del bosón Z.")
                elif answer_charge:
                    st.error("Incorrecto. Considera cómo la conservación de la carga funciona en los decaimientos. Leptone de carga opuesta son esperados en muchos decaimientos.")


                if n_leptons==2 and flavor=='Same' and charge=='Opposite':
                    st.session_state.is_z = True
                elif n_leptons==4 and flavor=='Same' and charge=='Opposite':
                    st.session_state.is_higgs = True
    
    # Step 4: Cuts on leptons pT only for Higgs
    if st.session_state.leptoncharge_cut_applied and st.session_state.is_higgs:
        st.markdown("## Cortes en el p$_T$ de los Leptones ")
        st.markdown("""En nuestra búsqueda por el **bosón de Higgs**, nos valemos de **cortes** que nos ayudan a encontrarlo en una vasta cantidad de datos. Una forma en la que podemos hacer esto es enfocandonos en una variable llamada **momento transverso** (p$_T$), que representa el momento de las partículas perpendiculas al eje del haz.

Cada lepton en nuestros datos tiene un valor de p$_T$, que hemos guardado en orden descendiente como **principal** (mayor p$_T$), **secundario**, y así sucesivamente. Al examinar estos valores, podemos aplicar cortes para sólo quedarnos con los datos con las características más parecidas a aquellas del bosón de Higgs, mientras eliminamos datos que es menos probable que lo contengan.

Una forma de aislar al Higgs es aplicar cortes que remuevan regiones donde el **fondo** (datos no relacionados al Higgs, pero con características similares) tienden a dominar, dejando más eventos que concuerda con una huella como la del Higgs. Esto significa establecer limites inferiores en el p$_T$ de los leptones, ya que mayores valores de p$_T$ values más probablemente capturen los eventos en los que estamos interesados.

Los gráficos siguientes muestran la distribución de p$_T$ del primer, segundo y tercer leptón en señal simulada (el Higgs que estamos buscando) y simulación del fondo. Aplicando cortes a los valores bajos de p$_T$ puede ayudar a reducir el fondo y mejorar la visibilidad de potenciales eventos del Higgs.
""")

        # Display initial image
        if not st.session_state['show_hint']:
            st.image(f"images/lepton_pt_{theme['base']}.png", caption="Distribución de pT de los tres leptones más energéticos en cada evento.")
        else:
            st.image(f"images/lepton_pt_{theme['base']}_lines.png", caption="istribución de pT de los tres leptones más energéticos en cada evento con posibles cortes.")

        st.markdown("Con esto en mente, consideremos los mejores cortes inferiores del p$_T$ que ayudarían a filtrar eventos de fondo mientras retenemos eventos que posiblmente son candidatos del Higgs.")
        with st.expander("🔍 Quiz", expanded=True):
            st.markdown("##### ⁉️ Selecciona Cortes Apropiados para el p$_T$ de los leptones.")

            st.markdown("""
            En base a lo discutido, ¿cuáles de los siguientes valores para cortes nos ayudarían a enfocarnos en eventos como los del Higgs, reduciendo el fondo?
            """)

            cut_options = [
                "20, 15, 10 ",
                "50, 45, 40",
                "2, 5, 10",
                "Ningún corte es necesario"
            ]

            answer_cut = st.radio("Selecciona la mejor opción para los cortes en p$_T$:", cut_options, index=None, key="pt_cut_quiz")
            
            st.button("¿Quieres una pista? Haz click aquí y revisa la imágen de arriba" if not st.session_state['show_hint'] else "Esconder pista", on_click=toggle_hint)
            # Checking for correct answer and providing feedback
            if answer_cut == cut_options[0]:
                st.success("¡Correcto! Establecer cortes en 20, 15, y 10 en los valores de p$_T$ de los leptones puede ayudar a enfocarnos en eventos similares a los del Higgs, filtrando eventos de fondo.")
            elif answer_cut:
                st.error("No realmente. Enfocate en los valores que efectivamente eliminarían fonda, todavía manteniendo la mayoría de la señal.")
            

        st.markdown("Ahora, hagamos los cortes:")

        if st.button("Corte en el p$_T$ de los leptones"):
            if st.session_state.leptonpt_cut_applied:
                st.toast("Ya aplicaste una selección. Para reiniciar el análisis ve al final de la página.", icon='❌')
            else:
                st.session_state.leptonpt_cut_applied = True
                # Display a spinner with the loading message
                random_sleep = random.randint(1, round(lumi/3))
                with st.spinner("Seleccionando eventos... Por favor espere."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                    st.session_state.leptoncharge_cut_applied = True

                    # Provide feedback to the user
                    st.toast("Selección aplicada exitosamente.", icon='✂️')
    
    if st.session_state.leptonpt_cut_applied:
        st.info(f"Eventos luego de la selección: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons']['nEvents']}")

    # Steep 5: invariant mass plot
    if (st.session_state.leptoncharge_cut_applied and not st.session_state.is_higgs) or (st.session_state.is_higgs and st.session_state.leptonpt_cut_applied):
        st.markdown("## Descubriendo Particulas con la Masa Invariante")
        st.markdown("La *masa invariante* es una herramienta importante en la física de partículas. Nos permite reconstruir la masa de las partículas que se producen en las colisiones, incluso cuando no las observamos directamente. Al analizar la energía y momento de los leptones en el estado final, podemos calcular su *masa invariante* combinada.")
        st.markdown("Al graficarla, la distribución de la masa invariante usualmente muestra picos donde las partículas como el bosón Z o el bosón de Higgs aparecen. Estos picos revelan la masa característica de la partícula, permitiéndonos \"verla\", incluso cuando ya decayó para el tiempo en el que estamos analizando los datos.")
        st.markdown("Al calcular y graficar la masa invariante, podrás observar estos picos y, potencialmente, ¡descubrir partículas por ti mismo!")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Masa Invariante")
            st.markdown("""
            La masa invariante es una cantidad importante en la física de partículas. ¿Qué nos puede decir sobre una partícula? 
            """)
            possible_mass = ["La energía de la partícula", 
                            "El momento de la partícula", 
                            "La masa en reposo de la partícula que produjo los leptones", 
                            "El tipo de partícula que decayó"]
            
            answer_mass = st.radio("Elige tu respuesta:", 
                                    possible_mass, 
                                    index=None, key="invariant_mass_selection_quiz")

            if answer_mass == possible_mass[2]:
                st.success("¡Correcto! La masa invariante nos dice la masa de la partícula que decayó en leptones.")
            elif answer_mass:
                st.error("Incorrecto. Recuerda, la masa invariante está relacionada con la masa en reposo de la partícula.")

        if st.button("Get invariant mass"):
            st.session_state.invariant_mass_calculated = True
    # Step 6: Discussion
    if st.session_state.invariant_mass_calculated:
        if st.session_state.is_higgs:
            st.image('analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_only_{theme['base']}"])
        else:
            st.image('analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}'][f"plot_data_only_{theme['base']}"])
        
        if not st.session_state.is_higgs:
            with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
                st.markdown("##### ⁉️ Interpretando el Gráfico de la Masa Invariante")
                st.markdown("""
                Generaste un gráfico de la masa invariante. Si un pico aparece alrededor de 91 GeV, a qué partícula puede que corresponda?
                """)

                possible_final = ["Bosón de Higgs", "Bosón Z", "Fotón", "Quark top"]
                answer_final = st.radio("Elige tu respuesta:", 
                                        possible_final, 
                                        index=None, key="invariant_mass_quiz")

                if answer_final == possible_final[1]:
                    st.success("¡Correcto! Un pico alrededor de 91 GeV tipicamente corresponde al bosón Z.")
                elif answer_final:
                    st.error("Incorrecto. Un pico alrededor de 91 GeV usualmente indican la presencia de un bosón Z, ya que 91 GeV es su masa.")
        
            if answer_final == possible_final[1]:
                if st.session_state.is_z:
                    st.balloons()
                st.markdown("### Discusión")
                st.markdown("Llegaste al final del análisis. Una vez que estés feliz con el resultado espera por la discusión, o resetea el análisis para intentar uno nuevo.")

        else:
            st.markdown("## ¿Cómo sabemos que hallamos el Higgs?")

            st.markdown("""
            Para determinar si hemos observado al bosón de Higgs, vamos a comparar nuestros datos del detectos con simulaciones de procesos de fondo conocidos y simulaciones de la señal. Esta aproximación nos permite ver si en nuestros datos se presenta un pico donde esperamos que aparezca el bosóns Higgs.
            """)

            # Step 1: Show data only
            st.markdown("### Paso 1: Observa los Datos")
            st.markdown("Empecemos observando únicamente los datos. Mira cuidadosamente: ¿notas alguna característica especial? Sin información adicional, puede ser difícil decir si alguno de los picos son debido a procesos de fondo o de señal.")
            higgs_data_only = 'analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_only_{theme['base']}"]
            st.image(higgs_data_only, caption="Únicamente datos del detector")

            # Quiz question for the data-only plot
            quiz_data = st.radio(
                "¿Qué observas en el gráfico con únicamente datos del detector?",
                options=["Un pico evidente", "Algunas fluctuaciones, pero es díficil decir", "Ninguna característica en particular"],
                index=None
            )
            if quiz_data == "Algunas fluctuaciones, pero es díficil decir":
                st.success("¡Exacto! Sin contexto, es difícil decir cuál fluctuacion es señal.")
            elif quiz_data == "Un pico evidente":
                st.warning("¿Ya encontraste el Higgs? Continuemos para ver si ese es el caso.")
            elif quiz_data == "Ninguna característica en particular":
                st.info("¡Vamos a aclarar con algunas simulaciones!")
            
            if quiz_data:
                # Step 2: Show data with background simulation
                st.markdown("### Paso 2: Añadimos Simulaciones de Fondo")
                st.markdown("Ahora, hemos añadido simulaciones de procesos de fondo (sin ninguna señal). Esto nos muestra lo que esperamos ver de otras partículas e interacciones en la ausencia del bosón de Higgs. Observa detalladamente: ¿hay algún pico que aparezca en adición al fondo?")
                higgs_data_bkg = 'analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_backgrounds_{theme['base']}"]
                st.image(higgs_data_bkg, caption="Datos del detector y simulación del fondo")

                # Quiz question for data with background
                quiz_background = st.radio(
                    "Con las simulaciones del fondo, ¿notas un pico adicional?",
                    options=["Sí, parece que hay un pico de más", "No, todo parece fondo", "No estoy seguro"],
                    index=None
                )
                if quiz_background == "Sí, parece que hay un pico de más":
                    st.success("Buena observación! Puede que estemos viendo algo más además del fondo.")
            
                if quiz_background:
                    # Step 3: Show data with background and simulated Higgs signal
                    st.markdown("### Paso 3: Agregamos la Simulación de la Señal del Higgs")
                    st.markdown("""
                    Finalmente, hemos agregado la simulación de la señal del bosón de Higgs para ver qué tan bien acuerda con los datos. Si los datos se alinean con el fondo más la simulación de la señal del Higgs, tenemos una fuerte evidencia de la existencia del bosón de Higgs. ¿Puedes ver un pico evidente donde esperamos el Higgs?
                    """)
                    higgs_data_bkg_sig = 'analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_backgrounds_signal_{theme['base']}"]
                    st.image(higgs_data_bkg_sig, caption="Datos con fondo y simulación de la señal del Higgs")

                    # Final quiz question
                    quiz_signal = st.radio(
                        "Al agregar la simulación de la señal del Higgs, ¿qué podemos concluir?",
                        options=["Hay un pico que concuerda con la señal del Higgs", "Todavía no es claro", "El fondo concuerda mejor con los datos"],
                        index=None
                    )
                    if quiz_signal == "Hay un pico que concuerda con la señal del Higgs":
                        st.success("¡Eso es correcto! La alineación del pico con la simulación de la señal del Higgs provee evidencia de que estamos observando el bosón de Higgs.")

                    if quiz_signal:
                        if quiz_signal == "Hay un pico que concuerda con la señal del Higgs":
                            st.balloons()
                        st.markdown("---")
                        st.markdown("### Discusión")
                        st.markdown("Llegaste al final del análisis. Una vez que estés feliz con el resultado espera por la discusión, o resetea el análisis para intentar uno nuevo.")
    

    # Reset button to start the analysis again
    st.markdown('---')
    st.write("""Si quieres volver a seleccionar eventos, haz click en el botón `Reset analysis`. 
             No te preocupes, ¡no necesitas volver a cargar los datos! Vas a empezar nuevamente en la selección del número de leptones.""")
    if st.button("Reset analysis"):
            # Reset flags
            st.session_state.nlepton_cut_applied = False
            st.session_state.leptontype_cut_applied = False
            st.session_state.leptoncharge_cut_applied = False
            st.session_state.leptonpt_cut_applied = False
            st.session_state.invariant_mass_calculated = False
            st.session_state.mc_loaded = False
            st.session_state.expand_all = False
            st.session_state.is_higgs = False
            st.session_state.is_z = False

            # Delete the widget keys from session_state
            for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()
            st.toast("El análisis ha sido reseteado.")