/**
 * Plugin which will use your default search engine (:h defsearch) to search
 * the domain you are currently browsing.  Also supports searching from your
 * web mail account.
 *
 * Usage:
 *   :search <search terms>
 *
 * Example mapping similar to 'o' or 't' to start the search command by typing
 * 's' in normal mode:
 *   map s :search<space>
 *
 * Another example which will attempt to grab the current query string, if you
 * are on the results page, and place it on the command line.
 *   map s <c-a-s>
 *
 * @author Eric Van Dewoetine (ervandew@gmail.com)
 * @author Laurent Bachelier (laurent@bachelier.name)
 * Overly simplified version compatible with pentadactyl
 * and with only the features I use.
 */

group.commands.add(["search"],
  "Search the current site using your default search engine.",
  function(args) {
    search.search(args.string);
  }
);

function Search() {
  return {
    'search': function(query) {
      var loc = window.content.document.location.toString();
      var domain = loc.replace(/[a-z]+:\/\/(.*?)\/.*/, '$1');

      var defsearch = options['defsearch'];

      events.feedkeys(':open ' + defsearch + ' site:' + domain + '<cr>');
    },

  };
}

var search = Search();
