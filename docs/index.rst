:html_theme.sidebar_secondary.remove:

================================================
GraphingLib Style Editor |release| documentation
================================================

.. raw:: html

    <style>
        .image-container {
            position: relative;
            width: 80%;
            margin: auto;
            height: 450px; /* Set a specific height for the container */
        }
        .large-image {
            width: 100%;
            height: auto;
            position: absolute;
            top: 0;
            left: 0;
            transition: opacity 1s ease-in-out;
            z-index: 1;
        }
        .fade-out {
            opacity: 0;
            z-index: 0;
        }
        .fade-in {
            opacity: 1;
            z-index: 2;
        }
        @media (max-width: 800px) {
            .image-container {
                height: 300px; 
            }
        }
        @media (max-width: 700px) {
            .image-container {
                height: 250px;
            }
        }
        @media (max-width: 600px) {
            .image-container {
                height: 250px; 
            }
        }
        @media (max-width: 400px) {
            .image-container {
                height: 200px; 
            }
        }
    </style>

    <div class="image-container">
        <img id="large-image1" class="large-image fade-in" src="_static/app_screenshots/figure_plain.png" alt="Image 1">
        <img id="large-image2" class="large-image fade-out" src="_static/app_screenshots/curve_dim.png" alt="Image 2">
    </div>

    <script>
        const imageSources = [
            '_static/app_screenshots/figure_plain.png',
            '_static/app_screenshots/curve_dim.png',
            '_static/app_screenshots/heatmap_custom.png',
            '_static/app_screenshots/histogram_dark.png',
            '_static/app_screenshots/polygon_plain.png',
            '_static/app_screenshots/figure_custom.png'
        ];

        let currentIndex = 0;
        const imageElement1 = document.getElementById('large-image1');
        const imageElement2 = document.getElementById('large-image2');

        function rotateImages() {
            currentIndex = (currentIndex + 1) % imageSources.length;
            const newImage = imageSources[currentIndex];

            if (imageElement1.classList.contains('fade-in')) {
                imageElement2.src = newImage;
                imageElement1.classList.remove('fade-in');
                imageElement1.classList.add('fade-out');
                imageElement2.classList.remove('fade-out');
                imageElement2.classList.add('fade-in');
            } else {
                imageElement1.src = newImage;
                imageElement2.classList.remove('fade-in');
                imageElement2.classList.add('fade-out');
                imageElement1.classList.remove('fade-out');
                imageElement1.classList.add('fade-in');
            }
        }

        setInterval(rotateImages, 5000);
    </script>




Quick start
-----------

Install GraphingLib Style Editor with **pip** :

.. code-block:: bash

    pip install glse

Install from `GitHub source code <https://github.com/GraphingLib/GraphingLibStyleEditor>`_ :

.. code-block:: bash

    pip install git+https://github.com/GraphingLib/GraphingLibStyleEditor.git

To open the Style Editor, in a terminal, enter

.. code-block:: bash

    glse

You can also open the Style Editor from a Python script as follows:

.. code-block:: python

    import glse
    
    glse.run()

It is as simple as that! You can now start creating your own styles for GraphingLib.

.. button-ref:: handbook
   :color: primary

        Go to Handbook


.. toctree::
   :maxdepth: 1
   :hidden:

   handbook
   Compatibility <compatibility>
   Back to GraphingLib <https://www.graphinglib.org/>
