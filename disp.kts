#!/usr/bin/env kscript
import java.io.File
import java.util.concurrent.TimeUnit
import java.util.Properties

private val resolutions_str = """
        resolution: 1920x1200, refresh rate: 0, HiDPI: True
        resolution: 1680x1050, refresh rate: 0, HiDPI: True
        resolution: 1440x900, refresh rate: 0, HiDPI: True
        resolution: 1280x800, refresh rate: 0, HiDPI: True
        resolution: 1024x640, refresh rate: 0, HiDPI: True
        resolution: 825x525, refresh rate: 0, HiDPI: True
        resolution: 720x450, refresh rate: 0, HiDPI: True
""".trimIndent()

private class Display {
    private class Resolution(properties: Map<String, String>) {
        val resolution: String by properties
        override fun toString(): String = "$resolution"
    }

    private val resolutions = decodeResolutions(resolutions_str)

    private fun decodeResolutions(content: String): List<Resolution> =
        content.split("\n")
            .map { it.trim() }
            .map { line ->
                val properties = line.split(", ").map { keyValue ->
                    val (key, value) = keyValue.split(": ")
                    key to value
                }.toMap()
                Resolution(properties)
            }


    fun main(args: Array<String>) {
        val arg0 = args.firstOrNull()
        if (arg0 == null) {
            help()
            return
        }
        val res = resolutions.getOrNull(arg0.toInt()) ?: kotlin.run {
            println("Index not found")
        }
        "display_manager.py res "
        val pids = getPidsForTcpPort(args.first().toInt())
        pids.forEach { pid ->
            println("Killing $pid")
            "kill $pid".runCommand().also { }
        }
    }


    private fun help() {
        println("Please, specify a valid index for a resolution:")
        resolutions.forEachIndexed { index, res ->
            println(" $index: $res")
        }
    }

}





fun String.runCommand(): String {

    val workingDir = File(".")
    val proc = ProcessBuilder(*split(" ").toTypedArray())
        .directory(workingDir)
        .redirectOutput(ProcessBuilder.Redirect.PIPE)
        .redirectError(ProcessBuilder.Redirect.PIPE)
        .start()

    proc.waitFor(1, TimeUnit.MINUTES)
    return proc.inputStream.bufferedReader().readText()
}

fun getPidsForTcpPort(port: Int): List<String> {
    val lsofOutput = "lsof -i tcp:$port".runCommand()

    if (lsofOutput.isBlank()) {
        println("No process is using $port")
        return emptyList()
    }

    println(lsofOutput)
    val lines = lsofOutput.split("\n")

    val header = lines.first()
    val headerValues = header.splitLines()
    check(headerValues[1] == "PID") { "expected header PID in `$header`" }
    val procs = lines.drop(1).filter { it.isNotBlank() }
    val pids = procs.map { it.splitLines()[1] }
    return pids
}

fun String.splitLines() = this.split(" ").filter { it.isNotBlank() }



Display().main(args)
