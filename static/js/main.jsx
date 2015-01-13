/*global $:false */
/*global React*/

(function () {
'use strict';

var TodoList = React.createClass({
  createTodo: function (item) {
    var done = item.complete ? 'done' : 'not-done';

    return  <div className={done}>
              <li className='todo-item' id={item.id}>
                <input type="checkbox" checked={item.complete} onChange={this.props.onUpdate.bind(null, item)} />
                {item.task}
                [<a href="#" onClick={this.props.onDelete.bind(null, item)}>x</a>]
              </li>
            </div>;

  },
  render: function () {
    return <ul className='todo-list'>{this.props.items.map(this.createTodo)}</ul>;
  }
});

var Footer = React.createClass({
  calculateTodosLeft: function (items) {
    var count = 0;
    for (var i = 0; i < items.length; i++) {
      if (!items[i].complete){
        count += 1;
      }
    }
    return count;
  },
  render : function () {
    return  <div className='footer-control'>
              <a>{this.calculateTodosLeft(this.props.items)} items left </a> 
              <div>
                <a href="#" onClick={this.props.onMarkAll.bind(null, this.props.items)}>Mark All done</a>
              </div>
            </div>;
  }
});

var TodoApp = React.createClass({
  getInitialState: function() {
    var items;
    $.ajax({
      url: "api_v1/todos/",
      success: function (data) {
          items = data;
      },
      dataType: 'json',
      async: false
    });
    return {items: items, text: ''};
  },

  onTextBoxChange: function (e) {
    this.setState({text: e.target.value});
  },

  onMarkAll: function (e) {
    this.state.items.map(function (item){
      item.complete = true;
      return item;
    });
    this.setState({items: this.state.items});

  },

  onUpdate: function (item, e) {
    var url = "api_v1/todos/".concat(item.id);
    var position = this.state.items.indexOf(item);

    this.state.items[position].complete = !this.state.items[position].complete;

    $.ajax({
      type: "PUT",
      url: url,
      context: this,
      success:  function () {
        this.setState({
          items: this.state.items, 
        });
      },
      data: JSON.stringify(this.state.items[position]),
      dataType: 'json',
      async: false
    });
  },

  onDelete: function (item, e) {
    var position = this.state.items.indexOf(item);
    var url = "api_v1/todos/".concat(item.id);

    if (~position) {
      $.ajax({
        type: "DELETE",
        url: url,
        dataType: 'json',
        async: false,
        context: this,
        success:  function (data) {
          this.state.items.splice(position, 1);
          this.setState({
            items: this.state.items, 
          });
        }
      });
    }    
  },

  onSubmit: function (e) {
    e.preventDefault();
    if (this.state.text) {
      var new_todo = {
        task: this.state.text,
        complete: false,
        id: null
      };

      $.ajax({
        type: "POST",
        url: "api_v1/todos/",
        data:  JSON.stringify(new_todo),
        dataType: 'json',
        async: false,
        context: this,
        success:  function (data) {
          new_todo.id = data.id;
          this.setState({
            items: this.state.items.concat([new_todo]), 
            text: ''
          });
        }
      });
    }
  },

  render: function () {
    return (
      <div>
        <div className='col-md-4 col-md-offset-4'>
          <h3 className='title'>Todos</h3>
          <hr className='dotted' />
          <form onSubmit={this.onSubmit}>
          <div className="input-group">
            <input className="form-control" type="text" onChange={this.onTextBoxChange} value={this.state.text} />
            <span className="input-group-btn">
              <input className="btn btn-default" type="submit">Add</input>
            </span>
          </div>
          </form>
          <div className='todo-list-container'>
            <TodoList items={this.state.items} onDelete={this.onDelete} onUpdate={this.onUpdate} />
          </div>
          <hr className='dotted' />
          <Footer items={this.state.items} onMarkAll={this.onMarkAll} />

        </div>
      </div>
    );
  }
});

React.render(<TodoApp />, document.body);

})();
