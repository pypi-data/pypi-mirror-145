Basic Usage of the ``comment`` Cube
===================================

Overview
++++++++

In order to attach a comment thread to an entity in your application, it suffices to add a
few lines of code to the ``call`` method of primary view of the entity.

Ideally, this code should perform the following steps:

1. check that the relation linking the entity to the comment thread is defined in the
   schema of the application. If so, also check that the entity is the object of 
   the relation checked.
2. if so, build a page section, as follows:

   #. pick up the context components from the current CubicWeb session's registry;
   #. from these components, select the ``'commentsection'`` view and apply it
      on the current result set (the set of comments).

3. render the page section built at 2.


Implementation Details
++++++++++++++++++++++

Assume in our schema we have an entity of (Yams) type ``'Subject'`` and we want to attach a comment
thread to it, via a relation named ``comments``.

For step 1, we want to:

1.1. pick up the schema::
     
     schema = self._cw.vreg.schema

1.2. check that the ``comments`` relation is in the schema and the ``Subject`` entity type is the object
     of the ``comments`` relation::

     if 'comments' in schema and 'Subject' in schema.rschema('comments').objects():

For step 2 (performed inside the ``if`` at 1.2), we want to build a section by 
selecting the ``commentsection`` view from the registry and applying the rset containing 
the comments to it::

    section = self._cw.vreg['ctxcomponents'].select('commentsection', self._cw, rset=self.cw_rset)

Finally, for step 3 (also performed inside the ``if`` at step 1.2), we render the section on 
the web page::

    section.render(w=self.w)

That's it!
     
     
