#!/usr/bin/env kscript

//INCLUDE common.kt
//INCLUDE detect_os.kt


fun main(args: Array<String>) {
    val port = args.firstOrNull()
    if (port == null) {
        println("Please, specify tcp port whose process will be killed")
        return
    }
    val pids = getPidsForTcpPort(args.first().toInt())
    pids.forEach { pid ->
        println("Killing $pid")
        "kill $pid".runCommand()
    }
}




//main(args)