import java.io.File
import java.util.concurrent.TimeUnit

fun String.runCommandInheritIO() {

    val proc = ProcessBuilder(*split(" ").toTypedArray())
        .inheritIO()
        .start()

    proc.waitFor(1, TimeUnit.MINUTES)
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

