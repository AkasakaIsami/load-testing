function json2obj(res) {
    return eval('(' + res + ')');
}

export {
    json2obj
}