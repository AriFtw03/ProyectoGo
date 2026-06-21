/*
  A validar:
  - Estructuras en bloque (var)
  - Declaraciones de funciones con retorno múltiple y closures
  - Gestión de errores léxicos específicos y límites
*/
package main

import "fmt"

func calculos(x int, y int) (int, float64) {
    suma := x + y
    division := float64(x) / 3.14
    return suma, division
}

func main() {
    // Declaración en bloque de variables
    var (
        a int = 5
        b string = "Prueba Go"
    )

    // Funciones anónimas o closures
    operacion := func(n int) int {
        return n * 2
    }

    resultadoSuma, resultadoFloat := calculos(a, 10)

    fmt.Println(b, operacion(a), resultadoSuma, resultadoFloat)

    // Error léxico simple
    @

    // Error de cadena sin cerrar
    cadenaInvalida := "Cadena de prueba que no cierra
}
