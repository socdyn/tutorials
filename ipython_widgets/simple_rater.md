Simple rater example with Notebook



```python
In[1]:  import ipywidgets as ipy
In[2]:  data = [
            {
                "predicted_rating": "4.6",
                "actual_rating": "",
                "title": "LOTR"
            },
            {
                "predicted_rating": "4.1",
                "actual_rating": "",
                "title": "A New Hope"
            },
            {
                "predicted_rating": "3.6",
                "actual_rating": "",
                "title": "Phantom Menace"
            }
        ]
In[3]:  class Rater:
            def __init__(self, data):
                self.data = [item.copy() for item in data]
                self.title_display = ipy.Label(description="Title", value="")
                self.rating_entry = ipy.Text(description="Rating", value="")

                self.previous_button = ipy.Button(description="<< Previous")
                self.next_button = ipy.Button(description="Next >>")
                self.done_button = ipy.Button(description="Done", disabled=True)

                self.rating_entry.observe(self.on_rating_changed, 'value')
                self.previous_button.on_click(self.on_previous)
                self.next_button.on_click(self.on_next)
                self.done_button.on_click(self.on_done)

                self.current_idx = 0
                self._update()

            def _ipython_display_(self):
                return ipy.VBox(
                    [
                        self.title_display,
                        self.rating_entry,
                        ipy.HBox(
                            [
                                self.previous_button,
                                self.next_button,
                                self.done_button,
                            ]
                        )
                    ]
                )._ipython_display_()

            def _update(self):
                self.title_display.value = self.data[self.current_idx]['title']
                self.rating_entry.value = self.data[self.current_idx]['actual_rating']
                if self.current_idx == 0:
                    self.previous_button.disabled = True
                    self.next_button.disabled = False
                elif self.current_idx == len(self.data) - 1:
                    self.previous_button.disabled = False
                    self.next_button.disabled = True


            def on_rating_changed(self, evt=None):
                self.data[self.current_idx]['actual_rating'] = self.rating_entry.value
                if all(item['actual_rating'] for item in self.data):
                    self.done_button.disabled = False

            def on_previous(self, evt=None):
                self.current_idx -= 1
                self._update()

            def on_next(self, evt=None):
                self.current_idx += 1
                self._update()

            def on_done(self, evt=None):
                self.rating_entry.disabled = True
                self.previous_button.disabled = True
                self.next_button.disabled = True
                self.done_button.disabled = True
In[4]:  r = Rater()
        r
In[5]:  r.data
```

If you put that class definition in a module, then notebook might be as simple as

```python
In[1]:  from movie_rater import Rater  
        data = [...]  
In[2]:  rater = Rater(data)  
        rater  
In[3]:  print(rater.data)  
```

Note: This was with

```
python=3.5.2
notebook=4.2.2
ipython=5.1.0
ipywidgets=5.2.2
```