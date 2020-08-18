function reset_form(form) {
    if (form.hasClass("was-validated")) {
        form.removeClass("was-validated");
    }
    form[0].reset();
}

var database = firebase.database();

var StateFact = function(state_fact, author_name, time_stamp, pinned) {
    this.fact = state_fact;
    this.author_name = author_name;
    this.time_stamp = time_stamp || new Date();
    this.pinned = pinned || false;
};

StateFact.prototype.to_json_ready = function() {
    return {
        state_fact: this.fact,
        author_name: this.author_name,
        time_stamp: this.time_stamp.toJSON(),
        pinned: this.pinned,
    };
};

function from_json_ready(fact_object) {
    var time_stamp = new Date(fact_object.time_stamp);
    return new StateFact(fact_object.state_fact, fact_object.author_name, 
                         time_stamp, fact_object.pinned);
}

var StateFactApp = function(node) {
    this.db_ref = database.ref("state-facts");
    this.fact_manager = new StateFactManager(node.find(".state-facts"), this.db_ref);
    this.add_fact_node = node.find("#fact-submit");
    this.fact_form = this.add_fact_node.find("form");
    this.fact_form.submit(this.add_fact.bind(this));
};

StateFactApp.prototype.store_fact = function(event, state_fact) {
    var reject_alert = this.fact_form.find("#database-reject-alert");
    var accept_func = function(fact_snapshot) {
        reject_alert.addClass("d-none");
        this.add_fact_node.modal("hide");
        reset_form(this.fact_form);
    };
    var reject_func = function(error) {
        event.preventDefault();
        event.stopPropagation();
        reject_alert.removeClass("d-none");
        this.fact_form.one("change", function() {
            reject_alert.addClass("d-none");
        });
    };
    this.db_ref.push(state_fact.to_json_ready()).then(
        accept_func.bind(this), reject_func.bind(this));
};

// change to list new facts first
// add filtering by state
// try to quickly tweak theme
// then basically done for now? 

StateFactApp.prototype.add_fact = function(event) {
    // validate form
    if (this.fact_form[0].checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        this.fact_form.toggleClass("was-validated");
        return;
    } 
    var fact = this.fact_form.find("textarea[name='fact']").first().val();
    var author_name = this.fact_form.find("input[name='author-name']").first().val();
    var state_fact = new StateFact(fact, author_name);
    this.store_fact(event, state_fact);
    return false;  // to prevent page reload
};

var StateFactManager = function(node, db_ref) {
    this.node = node;
    this.fact_template = node.find(".fact").clone();
    this.db_ref = db_ref;
    this.fact_index = 0;  // for fact enumeration
    // view all facts by default
    db_ref.orderByKey().on("child_added", this.view_fact.bind(this));
};

StateFactManager.prototype.view_fact = function(fact_snapshot, prev_fact_key) {
    var state_fact = from_json_ready(fact_snapshot.val());
    if (!state_fact.pinned) this.fact_index += 1;
   this.place_fact(state_fact, this.render_fact(state_fact));
};

StateFactManager.prototype.render_fact = function(state_fact) {
    var template = this.fact_template.clone();
    var fact_element = template.find(".text").first();
    var author_element = template.find(".author").first();
    fact_element.html("<p>" + state_fact.fact + "</p>");
    if (state_fact.pinned) {
        template.addClass("pinned");
    } else {
        template.removeClass("pinned");
        fact_element.find("p").prepend(
            "<span>" + this.fact_index.toString(10) + ". </span>");
    }
    author_element.text(state_fact.author_name);
    return template;
};

StateFactManager.prototype.place_fact = function(state_fact, fact_template) {
    // default to simply placing in the state-facts container
    if (state_fact.pinned) {
        this.node.prepend(fact_template);
    } else {
        this.node.append(fact_template);
    }
};

new StateFactApp($("#state-facts-app"));


