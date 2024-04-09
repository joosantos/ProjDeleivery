# Frontend for the kempo federation website

<p align="center">
  <img src="https://shields.io/badge/vue-^3.0.5-4FC08D?logo=vuedotjs&style=for-the-badge&logoColor=white" alt="vue">
  <img src="https://shields.io/badge/tailwind%20css-^3.3.2-06B6D4?logo=Tailwind%20CSS&style=for-the-badge&logoColor=white" alt="tailwind-css">
</p>

## Instalation

-   Donwload the project
    ```commandline
     git clone https://github.com/wygame-io/frontend
    ```
-   Install npm
    ```commandline
     cd /path/to/project
     npm install
    ```
-   Start the project:

    ```commandline
     npm run dev
    ```

-   .env file:
    -   All the variables must start with the prefix "VITE\_", ex.: "VITE_VAR_NAME"
    -   To use the variables in the code of the frontend use "import.meta.env.VITE_VAR_NAME"
    ```commandline
    VITE_API_URL=Endereço da api à qual o frontend irá fazer os pedidos
    ```
