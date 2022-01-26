function htmlEncode(str) {
    if (str === undefined || str == null) { return '' }
    return str.toString().replace(/[\u00A0-\u9999<>\&]/gim, function(i) {
            return '&#' + i.charCodeAt(0) + ';'
        })
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll("\"", "&quot;")
        .replaceAll("'", "&#39;");
}

function openTopic(e) {
    if (e === null) { return };
    let help_page = e.getAttribute('aria-opens');
    if (help_page) {
        get_page(help_page, document.getElementById("page"));
        return;
    }

    if (e.parentElement !== undefined) {
        openTopic(e.parentElement);
    }
}

function render_branch(branch, path) {
    let tree = "";
    for (let h = 0; h < branch.length; h++) {
        if (branch[h].children.length > 0) {
            tree += `<li><span class="caret">${branch[h].name}</span>
                        <ul class="nested">`;
            tree += render_branch(branch[h].children, `${path}/${branch[h].name}`);
            tree += `</ul></li>`
        } else {
            let display_name = branch[h].name.slice(0, -3);
            tree += `<li aria-opens="${htmlEncode(path + "/" + branch[h].name)}">${display_name}</li>`
        }
    }
    return tree
}

function get_topics(element) {
    let url = '/v1/docward'

    let execute = fetch(url, {
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => {
            if (response.status == "200") {
                response.json().then(function(topics) {
                    //tree = "";
                    //for (var h = 0; h < topics.length; h++) {
                    //    tree += `<div class="docward-topic" aria-opens="${htmlEncode(topics[h])}">${htmlEncode(topics[h])}</div>`
                    //}
                    //element.innerHTML = `<span id="docward-topic-tree">${tree}</span>`;

                    let result = [];
                    let level = { result };

                    topics.forEach(path => {
                        path.split('/').reduce((r, name, i, a) => {
                            if (!r[name]) {
                                r[name] = { result: [] };
                                r.result.push({ name, children: r[name].result })
                            }
                            return r[name];
                        }, level)
                    })

                    console.log(result)

                    element.innerHTML = `<span id="docward-topic-tree">
                                            <ul id="myUL">
                                                ${render_branch(result, '')}
                                            </ul>
                                        </span>`;

                    document.getElementById("docward-topic-tree").addEventListener('click', e => openTopic(e.target));
                    var toggler = document.getElementsByClassName("caret");
                    var i;

                    for (i = 0; i < toggler.length; i++) {
                        toggler[i].addEventListener("click", function() {
                            this.parentElement.querySelector(".nested").classList.toggle("active");
                            this.classList.toggle("caret-down");
                        });
                    }

                })
            } else {
                return response.text().then(response => {
                    error_object = JSON.parse(response).detail
                    error_object.error = error_object.error.replace(/([A-Z])/g, ' $1').trim()
                    throw new Error(JSON.stringify(error_object))
                })
            }
        })
        .catch(error => {
            console.log(error.message)
            errorObject = JSON.parse(error.message)
        });
}

function get_page(page, element) {
    let url = `/v1/docward/${page}`

    let execute = fetch(url, {
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => {
            if (response.status == "200") {
                response.text().then(function(md) {

                    let converter = new showdown.Converter({ tables: 'true' });
                    converter.setFlavor('github');
                    var html = converter.makeHtml(md);

                    element.innerHTML = html;

                })
            } else {
                return response.text().then(response => {
                    error_object = JSON.parse(response).detail
                    error_object.error = error_object.error.replace(/([A-Z])/g, ' $1').trim()
                    throw new Error(JSON.stringify(error_object))
                })
            }
        })
        .catch(error => {
            console.log(error.message)
            errorObject = JSON.parse(error.message)
        });
}