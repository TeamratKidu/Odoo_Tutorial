import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card };

    setup() {
        this.html = markup("<strong>Owl is awesome!</strong>");
        this.state = useState({
            count: 0,
        });
    }

    increment() {
        this.state.count++;
    }

}
